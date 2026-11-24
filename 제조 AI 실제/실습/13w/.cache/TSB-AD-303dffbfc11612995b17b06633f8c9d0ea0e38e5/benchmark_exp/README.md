### Scripts for running experiments / developing new methods in TSB-AD

* **Hyper-parameter Tuning**: `HP_Tuning_U.py` (univariate) / `HP_Tuning_M.py` (multivariate)

* **Benchmark Evaluation**: `Run_Detector_U.py` (univariate) / `Run_Detector_M.py` (multivariate)
    * Select the detector with `--AD_Name`, e.g. `python Run_Detector_U.py --AD_Name IForest`

* `benchmark_eval_results/`: Evaluation results of anomaly detectors across the time series in TSB-AD
    * All time series are normalized by z-score by default

---

## Develop your own algorithm

Your detector should subclass `BaseDetector` (`TSB_AD/models/base.py`) and expose:
* `fit(X)` and `decision_function(X)`, where `X` has shape `(n_samples, n_features)`
* a `decision_scores_` attribute (one anomaly score per timestamp; higher = more anomalous)

and be wrapped by a runner that returns a 1-D score array the same length as the input:
* `run_<Name>_Unsupervised(data, **HP)` — fits and scores the same series, **or**
* `run_<Name>_Semisupervised(data_train, data_test, **HP)` — fits on the (anomaly-free) train prefix, scores the test series

### The first way — submit a single self-contained script

Add one `Run_Custom_Detector.py`-style file in this folder (see `Run_Custom_Detector.py` for a template):
* **Step 1**: Implement the `Custom_AD` class
* **Step 2**: Implement the runner `run_Custom_AD_Unsupervised` or `run_Custom_AD_Semisupervised`
* **Step 3**: Specify the `Custom_AD_HP` hyper-parameter dict

### The second way — integrate into the repo (preferred for leaderboard inclusion)

* **Step 1**: Add `Custom_AD.py` under `TSB_AD/models/`
* **Step 2**: In `TSB_AD/model_wrapper.py`, add the runner `run_Custom_AD_Unsupervised` / `run_Custom_AD_Semisupervised`, **and** register the model name in `Unsupervise_AD_Pool` or `Semisupervise_AD_Pool` (the `Run_Detector_U/M.py` dispatcher raises if the name is in neither pool)
* **Step 3**: In `TSB_AD/HP_list.py`, add the hyper-parameters:
    * `Optimal_Uni_algo_HP_dict` / `Optimal_Multi_algo_HP_dict` — the single best config used by `Run_Detector_U/M.py` (required)
    * `Uni_algo_HP_dict` / `Multi_algo_HP_dict` — the search grid used by `HP_Tuning_U/M.py` (optional)
* **Step 4**: Apply a threshold to the anomaly score (if any)
* **Step 5**: Verify with `Run_Detector_U.py`/`Run_Detector_M.py` and submit your evaluation results [here](https://github.com/thedatumorg/TSB-AD/tree/main/benchmark_exp/leaderboard_results); once verified we will add it to the [🏆 Leaderboard](https://thedatumorg.github.io/TSB-AD/#leaderboard)

> 💡 Models are imported lazily inside `model_wrapper.py` (e.g. `from .models.Custom_AD import Custom_AD`), so a heavy or optional dependency only loads when its detector is actually selected.

🪧 **How to contribute your algorithm to TSB-AD**: open a pull request to the `main` branch following the steps above. We will test and evaluate the algorithm and include it in our [leaderboard](https://thedatumorg.github.io/TSB-AD/).
