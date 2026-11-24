# -*- coding: utf-8 -*-
# License: Apache-2.0 License

import math

import numpy as np
import pandas as pd

from .base import BaseDetector


EPS = 1e-12


def _as_univariate(X):
    arr = np.asarray(X, dtype=float)
    if arr.ndim == 1:
        return arr.reshape(-1)
    if arr.ndim == 2 and arr.shape[1] == 1:
        return arr[:, 0].reshape(-1)
    if arr.ndim == 2:
        raise ValueError(f"HSF_AD expects univariate input, got shape {arr.shape}")
    raise ValueError(f"HSF_AD expects a 1D or 2D array, got shape {arr.shape}")


def _clean_series(values):
    x = np.asarray(values, dtype=float).reshape(-1)
    if x.size == 0:
        return x

    finite = np.isfinite(x)
    if not finite.any():
        return np.zeros_like(x, dtype=float)

    finite_median = float(np.median(x[finite]))
    s = pd.Series(x).replace([np.inf, -np.inf], np.nan)
    s = s.interpolate(method="linear", limit_direction="both")
    s = s.fillna(finite_median)
    out = s.to_numpy(dtype=float)
    return np.nan_to_num(out, nan=finite_median, posinf=finite_median, neginf=finite_median)


def _safe_window(window, n):
    if n <= 1:
        return 1
    window = int(max(1, min(window, n)))
    return window


def _rolling_mean(values, window, center=True):
    x = _clean_series(values)
    window = _safe_window(window, x.size)
    if window <= 1:
        return x.copy()
    return (
        pd.Series(x)
        .rolling(window=window, min_periods=1, center=center)
        .mean()
        .to_numpy(dtype=float)
    )


def _rolling_std(values, window, center=True):
    x = _clean_series(values)
    window = _safe_window(window, x.size)
    if window <= 1:
        return np.zeros_like(x)
    out = (
        pd.Series(x)
        .rolling(window=window, min_periods=2, center=center)
        .std(ddof=0)
        .to_numpy(dtype=float)
    )
    return _clean_series(out)


def _rolling_corr_lag(values, lag, window, center=True):
    x = _clean_series(values)
    n = x.size
    if n <= 2 or lag <= 0 or lag >= n:
        return np.zeros(n, dtype=float)

    lagged = np.empty(n, dtype=float)
    lagged[:lag] = np.nan
    lagged[lag:] = x[:-lag]
    corr = (
        pd.Series(x)
        .rolling(window=_safe_window(window, n), min_periods=3, center=center)
        .corr(pd.Series(lagged))
        .to_numpy(dtype=float)
    )
    return np.nan_to_num(corr, nan=0.0, posinf=0.0, neginf=0.0)


def _shift(values, periods, fill_value=0.0):
    x = np.asarray(values, dtype=float).reshape(-1)
    out = np.empty_like(x)
    if periods == 0 or x.size == 0:
        return x.copy()
    if abs(periods) >= x.size:
        out.fill(fill_value)
        return out
    if periods > 0:
        out[:periods] = fill_value
        out[periods:] = x[:-periods]
    else:
        p = abs(periods)
        out[-p:] = fill_value
        out[:-p] = x[p:]
    return out


def _ewma(values, span):
    x = _clean_series(values)
    span = max(1, int(span))
    return pd.Series(x).ewm(span=span, adjust=False).mean().to_numpy(dtype=float)


def _robust_positive_feature(values):
    x = _clean_series(values)
    if x.size == 0:
        return x
    median = float(np.median(x))
    mad = float(np.median(np.abs(x - median)))
    scale = 1.4826 * mad
    if not np.isfinite(scale) or scale < EPS:
        scale = float(np.std(x))
    if not np.isfinite(scale) or scale < EPS:
        return np.zeros_like(x, dtype=float)
    z = (x - median) / scale
    z = np.nan_to_num(z, nan=0.0, posinf=0.0, neginf=0.0)
    return np.clip(np.maximum(z, 0.0), 0.0, 50.0)


def _combine_proxy_features(feature_list, n):
    scaled = []
    for feature in feature_list:
        arr = np.asarray(feature, dtype=float).reshape(-1)
        if arr.size != n:
            raise ValueError("Proxy feature length mismatch")
        scaled.append(_robust_positive_feature(arr))
    if not scaled:
        return np.zeros(n, dtype=float)
    return _clean_series(np.mean(np.vstack(scaled), axis=0))


def _causal_robust_positive_feature(values, window):
    x = _clean_series(values)
    if x.size == 0:
        return x
    if np.std(x) < EPS:
        return np.zeros_like(x, dtype=float)

    window = _safe_window(window, x.size)
    s = pd.Series(x)
    median = s.rolling(window=window, min_periods=1, center=False).median()
    abs_dev = (s - median).abs()
    mad = abs_dev.rolling(window=window, min_periods=1, center=False).median()
    scale = 1.4826 * mad

    rolling_std = s.rolling(window=window, min_periods=2, center=False).std(ddof=0)
    expanding_std = s.expanding(min_periods=2).std(ddof=0)
    scale = scale.where(scale >= EPS, rolling_std)
    scale = scale.where(scale >= EPS, expanding_std)
    scale = scale.replace([np.inf, -np.inf], np.nan)

    z = (s - median) / scale.replace(0.0, np.nan)
    z = z.replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=float)
    return np.clip(np.maximum(z, 0.0), 0.0, 50.0)


def _combine_proxy_features_causal(feature_list, n, window):
    scaled = []
    for feature in feature_list:
        arr = np.asarray(feature, dtype=float).reshape(-1)
        if arr.size != n:
            raise ValueError("Proxy feature length mismatch")
        scaled.append(_causal_robust_positive_feature(arr, window))
    if not scaled:
        return np.zeros(n, dtype=float)
    return _clean_series(np.mean(np.vstack(scaled), axis=0))


def _safe_minmax(values):
    x = _clean_series(values)
    if x.size == 0:
        return x
    min_v = float(np.min(x))
    max_v = float(np.max(x))
    if not np.isfinite(min_v) or not np.isfinite(max_v) or max_v - min_v < EPS:
        return np.zeros_like(x, dtype=float)
    return (x - min_v) / (max_v - min_v)


def _safe_expanding_minmax(values):
    x = _clean_series(values)
    if x.size == 0:
        return x
    s = pd.Series(x)
    min_v = s.expanding(min_periods=1).min()
    max_v = s.expanding(min_periods=1).max()
    denom = max_v - min_v
    out = (s - min_v) / denom.replace(0.0, np.nan)
    out = out.where(denom >= EPS, 0.0)
    return out.replace([np.inf, -np.inf], np.nan).fillna(0.0).to_numpy(dtype=float)


def _estimate_ar1_phi(values):
    x = _clean_series(values)
    if x.size < 3 or np.std(x) < EPS:
        return 0.0
    centered = x - float(np.median(x))
    prev = centered[:-1]
    curr = centered[1:]
    denom = float(np.dot(prev, prev))
    if denom < EPS:
        return 0.0
    phi = float(np.dot(prev, curr) / denom)
    if not np.isfinite(phi):
        return 0.0
    return float(np.clip(phi, -0.99, 0.99))


def _estimate_period(values, max_lag=256, min_lag=2, threshold=0.35):
    x = _clean_series(values)
    n = x.size
    if n < 12 or np.std(x) < EPS:
        return None

    x = x - float(np.median(x))
    max_lag = int(min(max_lag, max(min_lag, n // 2)))
    if max_lag <= min_lag:
        return None

    best_lag = None
    best_corr = -np.inf
    for lag in range(min_lag, max_lag + 1):
        a = x[:-lag]
        b = x[lag:]
        if a.size < 3 or np.std(a) < EPS or np.std(b) < EPS:
            continue
        corr = float(np.corrcoef(a, b)[0, 1])
        if np.isfinite(corr) and corr > best_corr:
            best_lag = lag
            best_corr = corr

    if best_lag is None or best_corr < threshold:
        return None
    return int(best_lag)


def _spectral_samples(values, window, stride):
    x = _clean_series(values)
    n = x.size
    if n < 4:
        return np.zeros((0, 3), dtype=float), np.zeros(0, dtype=float), np.zeros(0, dtype=int)

    window = _safe_window(window, n)
    stride = max(1, int(stride))
    centers = np.arange(0, n, stride, dtype=int)
    if centers.size == 0 or centers[-1] != n - 1:
        centers = np.append(centers, n - 1)

    half = max(1, window // 2)
    distributions = []
    entropies = []

    for center in centers:
        start = max(0, int(center) - half)
        end = min(n, int(center) + half + 1)
        segment = x[start:end]
        if segment.size < 4 or np.std(segment) < EPS:
            distributions.append(np.zeros(3, dtype=float))
            entropies.append(0.0)
            continue

        segment = segment - float(np.mean(segment))
        tapered = segment * np.hanning(segment.size)
        power = np.abs(np.fft.rfft(tapered)) ** 2
        power = power[1:]
        total = float(np.sum(power))
        if power.size == 0 or total < EPS:
            distributions.append(np.zeros(3, dtype=float))
            entropies.append(0.0)
            continue

        bands = np.array_split(power, 3)
        band_energy = np.array([float(np.sum(band)) for band in bands], dtype=float)
        distribution = band_energy / max(float(np.sum(band_energy)), EPS)
        p = power / total
        entropy = -float(np.sum(p * np.log(p + EPS))) / math.log(max(power.size, 2))
        distributions.append(distribution)
        entropies.append(entropy)

    return np.vstack(distributions), np.asarray(entropies, dtype=float), centers


def _interpolate_samples(values, centers, n):
    values = np.asarray(values, dtype=float).reshape(-1)
    centers = np.asarray(centers, dtype=float).reshape(-1)
    if n == 0:
        return np.zeros(0, dtype=float)
    if values.size == 0 or centers.size == 0:
        return np.zeros(n, dtype=float)
    if values.size == 1:
        return np.full(n, float(values[0]), dtype=float)
    return np.interp(np.arange(n, dtype=float), centers, values)


def _hsf_weights(HP=None):
    hp = HP or {}
    weights = hp.get("weights")
    if weights is None:
        weights = [
            hp.get("w1", 1.0),
            hp.get("w2", 1.0),
            hp.get("w3", 1.0),
            hp.get("w4", 1.0),
            hp.get("w5", 1.0),
        ]
    weights = np.asarray(weights, dtype=float).reshape(-1)
    if weights.size != 5 or not np.isfinite(weights).all():
        return np.ones(5, dtype=float)
    return weights


def _default_hsf_windows(n, HP=None):
    hp = HP or {}
    default_window = int(min(256, max(16, n // 20))) if n >= 16 else max(1, n)
    window = _safe_window(hp.get("window", default_window), n)
    short_window = _safe_window(hp.get("short_window", max(5, window // 4)), n)
    long_window = _safe_window(hp.get("long_window", max(window, window * 2)), n)
    spectral_window = _safe_window(hp.get("spectral_window", max(16, window)), n)
    spectral_stride = max(
        1, int(hp.get("spectral_stride", max(1, spectral_window // 4)))
    )
    return window, short_window, long_window, spectral_window, spectral_stride


def _spectral_distribution(segment):
    segment = _clean_series(segment)
    if segment.size < 4 or np.std(segment) < EPS:
        return np.zeros(3, dtype=float), 0.0

    segment = segment - float(np.mean(segment))
    tapered = segment * np.hanning(segment.size)
    power = np.abs(np.fft.rfft(tapered)) ** 2
    power = power[1:]
    total = float(np.sum(power))
    if power.size == 0 or total < EPS:
        return np.zeros(3, dtype=float), 0.0

    bands = np.array_split(power, 3)
    band_energy = np.array([float(np.sum(band)) for band in bands], dtype=float)
    distribution = band_energy / max(float(np.sum(band_energy)), EPS)
    p = power / total
    entropy = -float(np.sum(p * np.log(p + EPS))) / math.log(max(power.size, 2))
    return distribution, entropy


def _rolling_spectral_proxy_causal(x, window, stride, baseline_alpha=0.1):
    x = _clean_series(x)
    n = x.size
    signature_deviation = np.zeros(n, dtype=float)
    entropy_deviation = np.zeros(n, dtype=float)
    high_band_share = np.zeros(n, dtype=float)
    if n < 4:
        return {
            "signature_deviation": signature_deviation,
            "entropy_deviation": entropy_deviation,
            "high_band_share": high_band_share,
        }

    window = _safe_window(window, n)
    stride = max(1, int(stride))
    endpoints = np.arange(0, n, stride, dtype=int)
    if endpoints.size == 0 or endpoints[-1] != n - 1:
        endpoints = np.append(endpoints, n - 1)

    alpha = float(np.clip(baseline_alpha, 0.001, 1.0))
    baseline_signature = None
    baseline_entropy = 0.0
    prev_endpoint = -1
    last_sig_dev = 0.0
    last_entropy_dev = 0.0
    last_high_share = 0.0

    for endpoint in endpoints:
        endpoint = int(endpoint)
        if endpoint > prev_endpoint + 1:
            start_hold = prev_endpoint + 1
            signature_deviation[start_hold:endpoint] = last_sig_dev
            entropy_deviation[start_hold:endpoint] = last_entropy_dev
            high_band_share[start_hold:endpoint] = last_high_share

        start = max(0, endpoint - window + 1)
        distribution, entropy = _spectral_distribution(x[start : endpoint + 1])
        if baseline_signature is None:
            sig_dev = 0.0
            entropy_dev = 0.0
            baseline_signature = distribution.copy()
            baseline_entropy = float(entropy)
        else:
            sig_dev = float(np.sum(np.abs(distribution - baseline_signature)))
            entropy_dev = abs(float(entropy) - baseline_entropy)
            baseline_signature = (
                alpha * distribution + (1.0 - alpha) * baseline_signature
            )
            total = float(np.sum(baseline_signature))
            if total > EPS:
                baseline_signature = baseline_signature / total
            baseline_entropy = alpha * float(entropy) + (1.0 - alpha) * baseline_entropy

        last_sig_dev = sig_dev
        last_entropy_dev = entropy_dev
        last_high_share = float(distribution[-1])
        signature_deviation[endpoint] = last_sig_dev
        entropy_deviation[endpoint] = last_entropy_dev
        high_band_share[endpoint] = last_high_share
        prev_endpoint = endpoint

    return {
        "signature_deviation": signature_deviation,
        "entropy_deviation": entropy_deviation,
        "high_band_share": high_band_share,
    }


def _causal_ar_prediction(x, window, long_window):
    x = _clean_series(x)
    n = x.size
    if n == 0:
        return np.zeros(0, dtype=float)
    if n == 1:
        return x.copy()

    baseline = _ewma(x, long_window)
    baseline_prev = _shift(baseline, 1, fill_value=x[0])
    previous = _shift(x, 1, fill_value=x[0])

    pair_prev = previous - baseline_prev
    pair_curr = x - baseline
    numerator = _rolling_mean(pair_prev * pair_curr, window, center=False)
    denominator = _rolling_mean(pair_prev ** 2, window, center=False)
    phi_raw = np.divide(
        numerator,
        denominator,
        out=np.zeros_like(numerator),
        where=denominator > EPS,
    )
    phi_raw = np.clip(np.nan_to_num(phi_raw, nan=0.0, posinf=0.0, neginf=0.0), -0.99, 0.99)
    phi = _shift(phi_raw, 1, fill_value=0.0)
    return baseline_prev + phi * (previous - baseline_prev)


class HSF_AD(BaseDetector):
    """HSF-inspired detector built from robust univariate proxy features."""

    def __init__(self, HP=None, normalize=True):
        super().__init__()
        self.HP = HP or {}
        self.normalize = normalize

    def fit(self, X, y=None):
        x = _clean_series(_as_univariate(X))
        self._configure_from_training(x)
        self.decision_scores_ = self._score_series(x)
        return self

    def decision_function(self, X):
        x = _clean_series(_as_univariate(X))
        return self._score_series(x)

    def _configure_from_training(self, x):
        n = x.size
        default_window = int(min(256, max(16, n // 20))) if n >= 16 else max(1, n)
        self.window_ = _safe_window(self.HP.get("window", default_window), n)
        self.short_window_ = _safe_window(
            self.HP.get("short_window", max(5, self.window_ // 4)), n
        )
        self.long_window_ = _safe_window(
            self.HP.get("long_window", max(self.window_, self.window_ * 2)), n
        )
        self.spectral_window_ = _safe_window(
            self.HP.get("spectral_window", max(16, self.window_)), n
        )
        self.spectral_stride_ = max(
            1, int(self.HP.get("spectral_stride", max(1, self.spectral_window_ // 4)))
        )

        weights = self.HP.get("weights")
        if weights is None:
            weights = [
                self.HP.get("w1", 1.0),
                self.HP.get("w2", 1.0),
                self.HP.get("w3", 1.0),
                self.HP.get("w4", 1.0),
                self.HP.get("w5", 1.0),
            ]
        weights = np.asarray(weights, dtype=float).reshape(-1)
        if weights.size != 5 or not np.isfinite(weights).all():
            weights = np.ones(5, dtype=float)
        self.weights_ = weights

        self.center_ = float(np.median(x)) if n else 0.0
        self.phi_ = _estimate_ar1_phi(x)
        self.period_ = _estimate_period(x, max_lag=self.HP.get("max_period_lag", 256))
        acorr1 = _rolling_corr_lag(x, lag=1, window=self.window_)
        self.acorr1_baseline_ = float(np.median(acorr1)) if acorr1.size else 0.0

        distributions, entropies, _ = _spectral_samples(
            x, self.spectral_window_, self.spectral_stride_
        )
        if distributions.size:
            signature = np.median(distributions, axis=0)
            total = float(np.sum(signature))
            self.spectral_signature_ = (
                signature / total if total > EPS else np.zeros(3, dtype=float)
            )
            self.spectral_entropy_ = float(np.median(entropies))
        else:
            self.spectral_signature_ = np.zeros(3, dtype=float)
            self.spectral_entropy_ = 0.0

    def _score_series(self, x):
        n = x.size
        if n == 0:
            self.components_ = {}
            return np.zeros(0, dtype=float)
        if np.std(x) < EPS:
            self.components_ = {
                "K1_proxy": np.zeros(n, dtype=float),
                "K2_coupling_proxy": np.zeros(n, dtype=float),
                "K3_collective_proxy": np.zeros(n, dtype=float),
                "K4_retuning_proxy": np.zeros(n, dtype=float),
                "C5_closure_proxy": np.zeros(n, dtype=float),
            }
            return np.zeros(n, dtype=float)

        window = _safe_window(getattr(self, "window_", 16), n)
        short_window = _safe_window(getattr(self, "short_window_", 5), n)
        long_window = _safe_window(getattr(self, "long_window_", window), n)

        diff = np.abs(np.diff(x, prepend=x[0]))
        first_diff = np.diff(x, prepend=x[0])
        jerk = np.abs(np.diff(first_diff, prepend=first_diff[0]))
        local_mean = _rolling_mean(x, short_window)
        residual = x - local_mean
        residual_abs = np.abs(residual)
        residual_energy = _rolling_mean(residual ** 2, short_window)
        diff_energy = _rolling_mean(diff ** 2, short_window)

        K1_proxy = _combine_proxy_features(
            [diff, jerk, residual_abs, residual_energy, diff_energy], n
        )

        acorr1 = _rolling_corr_lag(x, lag=1, window=window)
        acorr_baseline = getattr(self, "acorr1_baseline_", 0.0)
        acorr_deviation = np.abs(acorr1 - acorr_baseline)
        acorr_instability = np.abs(np.diff(acorr1, prepend=acorr1[0]))
        signal_center = x - _rolling_mean(x, long_window)
        signal_energy = _rolling_mean(signal_center ** 2, window)
        residual_energy_window = _rolling_mean(residual ** 2, window)
        energy_ratio = residual_energy_window / (signal_energy + EPS)
        quiet = (signal_energy < EPS) & (residual_energy_window < EPS)
        energy_ratio[quiet] = 0.0

        K2_coupling_proxy = _combine_proxy_features(
            [acorr_deviation, acorr_instability, energy_ratio], n
        )

        spectral = self._rolling_spectral_proxy(x)
        K3_collective_proxy = _combine_proxy_features(
            [
                spectral["signature_deviation"],
                spectral["entropy_deviation"],
                spectral["high_band_share"],
            ],
            n,
        )

        impulse = diff + jerk
        delayed_impulse = _shift(_ewma(impulse, short_window), 1, fill_value=0.0)
        recovery_error = delayed_impulse * residual_abs
        residual_persistence = _rolling_mean(residual_abs, long_window)
        decay_lag = min(max(2, short_window), max(2, n - 1))
        acorr_decay = np.abs(_rolling_corr_lag(x, lag=decay_lag, window=long_window))
        fast_residual = _ewma(residual ** 2, short_window)
        slow_residual = _ewma(residual ** 2, long_window)
        tail_energy = np.maximum(slow_residual - fast_residual, 0.0)

        K4_retuning_proxy = _combine_proxy_features(
            [recovery_error, residual_persistence, acorr_decay, tail_energy], n
        )

        previous = _shift(x, 1, fill_value=self.center_)
        ar_prediction = self.center_ + getattr(self, "phi_", 0.0) * (previous - self.center_)
        ar_residual = np.abs(x - ar_prediction)
        ewma_prediction = _shift(_ewma(x, short_window), 1, fill_value=self.center_)
        ewma_residual = np.abs(x - ewma_prediction)
        predictability_error = _rolling_mean(ar_residual ** 2, window)
        period = getattr(self, "period_", None)
        if period is not None and period < n:
            periodic_error = np.abs(x - _shift(x, period, fill_value=self.center_))
            repeatability_error = np.abs(impulse - _shift(impulse, period, fill_value=0.0))
        else:
            periodic_error = ewma_residual
            repeatability_error = _rolling_std(impulse, window) / (
                _rolling_mean(np.abs(impulse), window) + EPS
            )

        C5_closure_proxy = _combine_proxy_features(
            [ar_residual, ewma_residual, predictability_error, periodic_error, repeatability_error],
            n,
        )

        self.components_ = {
            "K1_proxy": K1_proxy,
            "K2_coupling_proxy": K2_coupling_proxy,
            "K3_collective_proxy": K3_collective_proxy,
            "K4_retuning_proxy": K4_retuning_proxy,
            "C5_closure_proxy": C5_closure_proxy,
        }

        stacked = np.vstack(
            [
                K1_proxy,
                K2_coupling_proxy,
                K3_collective_proxy,
                K4_retuning_proxy,
                C5_closure_proxy,
            ]
        )
        score = np.dot(self.weights_, stacked)
        return _clean_series(score)

    def _rolling_spectral_proxy(self, x):
        n = x.size
        distributions, entropies, centers = _spectral_samples(
            x,
            _safe_window(getattr(self, "spectral_window_", 16), n),
            getattr(self, "spectral_stride_", 4),
        )
        if distributions.size == 0:
            return {
                "signature_deviation": np.zeros(n, dtype=float),
                "entropy_deviation": np.zeros(n, dtype=float),
                "high_band_share": np.zeros(n, dtype=float),
            }

        baseline_signature = getattr(self, "spectral_signature_", np.zeros(3, dtype=float))
        baseline_entropy = getattr(self, "spectral_entropy_", 0.0)
        signature_deviation = np.sum(np.abs(distributions - baseline_signature), axis=1)
        entropy_deviation = np.abs(entropies - baseline_entropy)
        high_band_share = distributions[:, -1]

        return {
            "signature_deviation": _interpolate_samples(signature_deviation, centers, n),
            "entropy_deviation": _interpolate_samples(entropy_deviation, centers, n),
            "high_band_share": _interpolate_samples(high_band_share, centers, n),
        }


def run_HSF_AD_Unsupervised(data, HP=None):
    clf = HSF_AD(HP=HP)
    clf.fit(data)
    return _safe_minmax(clf.decision_scores_)


def run_HSF_AD_Semisupervised(data_train, data_test, HP=None):
    clf = HSF_AD(HP=HP)
    clf.fit(data_train)
    return _safe_minmax(clf.decision_function(data_test))


def run_HSF_AD_Causal(data, HP=None):
    x = _clean_series(_as_univariate(data))
    n = x.size
    if n == 0:
        return np.zeros(0, dtype=float)
    if np.std(x) < EPS:
        return np.zeros(n, dtype=float)

    hp = HP or {}
    window, short_window, long_window, spectral_window, spectral_stride = (
        _default_hsf_windows(n, hp)
    )
    weights = _hsf_weights(hp)

    diff = np.abs(np.diff(x, prepend=x[0]))
    first_diff = np.diff(x, prepend=x[0])
    jerk = np.abs(np.diff(first_diff, prepend=first_diff[0]))
    local_mean = _rolling_mean(x, short_window, center=False)
    residual = x - local_mean
    residual_abs = np.abs(residual)
    residual_energy = _rolling_mean(residual ** 2, short_window, center=False)
    diff_energy = _rolling_mean(diff ** 2, short_window, center=False)

    K1_proxy = _combine_proxy_features_causal(
        [diff, jerk, residual_abs, residual_energy, diff_energy], n, window
    )

    acorr1 = _rolling_corr_lag(x, lag=1, window=window, center=False)
    acorr_baseline = _shift(
        _rolling_mean(acorr1, long_window, center=False), 1, fill_value=0.0
    )
    acorr_deviation = np.abs(acorr1 - acorr_baseline)
    acorr_instability = np.abs(np.diff(acorr1, prepend=acorr1[0]))
    signal_center = x - _rolling_mean(x, long_window, center=False)
    signal_energy = _rolling_mean(signal_center ** 2, window, center=False)
    residual_energy_window = _rolling_mean(residual ** 2, window, center=False)
    energy_ratio = residual_energy_window / (signal_energy + EPS)
    quiet = (signal_energy < EPS) & (residual_energy_window < EPS)
    energy_ratio[quiet] = 0.0

    K2_coupling_proxy = _combine_proxy_features_causal(
        [acorr_deviation, acorr_instability, energy_ratio], n, window
    )

    spectral = _rolling_spectral_proxy_causal(
        x,
        spectral_window,
        spectral_stride,
        baseline_alpha=hp.get("spectral_baseline_alpha", 0.1),
    )
    K3_collective_proxy = _combine_proxy_features_causal(
        [
            spectral["signature_deviation"],
            spectral["entropy_deviation"],
            spectral["high_band_share"],
        ],
        n,
        window,
    )

    impulse = diff + jerk
    delayed_impulse = _shift(_ewma(impulse, short_window), 1, fill_value=0.0)
    recovery_error = delayed_impulse * residual_abs
    residual_persistence = _rolling_mean(residual_abs, long_window, center=False)
    decay_lag = min(max(2, short_window), max(2, n - 1))
    acorr_decay = np.abs(
        _rolling_corr_lag(x, lag=decay_lag, window=long_window, center=False)
    )
    fast_residual = _ewma(residual ** 2, short_window)
    slow_residual = _ewma(residual ** 2, long_window)
    tail_energy = np.maximum(slow_residual - fast_residual, 0.0)

    K4_retuning_proxy = _combine_proxy_features_causal(
        [recovery_error, residual_persistence, acorr_decay, tail_energy], n, window
    )

    ar_prediction = _causal_ar_prediction(x, window, long_window)
    ar_residual = np.abs(x - ar_prediction)
    ewma_prediction = _shift(_ewma(x, short_window), 1, fill_value=x[0])
    ewma_residual = np.abs(x - ewma_prediction)
    predictability_error = _rolling_mean(ar_residual ** 2, window, center=False)
    repeatability_error = _rolling_std(impulse, window, center=False) / (
        _rolling_mean(np.abs(impulse), window, center=False) + EPS
    )

    C5_closure_proxy = _combine_proxy_features_causal(
        [ar_residual, ewma_residual, predictability_error, ewma_residual, repeatability_error],
        n,
        window,
    )

    stacked = np.vstack(
        [
            K1_proxy,
            K2_coupling_proxy,
            K3_collective_proxy,
            K4_retuning_proxy,
            C5_closure_proxy,
        ]
    )
    return _safe_expanding_minmax(np.dot(weights, stacked))
