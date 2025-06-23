# 개발 환경 및 Docker 컨테이너 사용 설명서

이 문서는 `nvcr.io/nvidia/tensorflow:25.02-tf2-py3` Docker 이미지를 기반으로 한 개발 환경 설정 및 사용 방법을 안내합니다.

## 1. 개발 환경

- **OS**: Ubuntu 25.04
- **GPU**: NVIDIA GeForce RTX 5070 Ti 16GB
- **메모리**: 32GB
- **NVIDIA 드라이버 버전**: 570.169
- **CUDA 버전**: 12.8
- **주요 프레임워크**: PyTorch, TensorFlow, Detectron2
- **개발 도구**: PyCharm

## 2. Docker 컨테이너 실행

### 사전 요구 사항
- **Docker** 및 **NVIDIA Container Toolkit**가 설치되어 있어야 합니다.

### Docker 데몬 설정 (`/etc/docker/daemon.json`)
Docker가 NVIDIA 런타임을 사용하도록 설정합니다.
```json
{
    "runtimes": {
        "nvidia": {
            "path": "nvidia-container-runtime",
            "runtimeArgs": []
        }
    }
}
```
> 설정 변경 후에는 `sudo systemctl restart docker` 명령어로 Docker 데몬을 재시작하세요.

### 기본 컨테이너 실행
```bash
docker run --gpus all -it --rm nvcr.io/nvidia/tensorflow:25.02-tf2-py3
```

### Jupyter Notebook 서버 실행
현재 디렉터리를 공유하는 Jupyter Notebook 서버를 실행합니다.
```bash
docker run --gpus all -it --rm \
  -p 8888:8888 \
  -v $(pwd):/workspace \
  nvcr.io/nvidia/tensorflow:25.02-tf2-py3 \
  jupyter notebook --ip=0.0.0.0 --port=8888 --allow-root --NotebookApp.token=''
```
> 실행 후, 웹 브라우저에서 `http://localhost:8888` 로 접속하여 사용할 수 있습니다.

## 3. 설치된 라이브러리 전체 목록

| Package | Version |
|---|---|
| absl-py | 1.0.0 |
| aiohappyeyeballs | 2.4.4 |
| aiohttp | 3.11.11 |
| aiosignal | 1.3.2 |
| anyio | 4.8.0 |
| argon2-cffi | 23.1.0 |
| argon2-cffi-bindings | 21.2.0 |
| array_record | 0.7.2 |
| arrow | 1.3.0 |
| asciitree | 0.3.3 |
| asttokens | 3.0.0 |
| astunparse | 1.6.3 |
| async-lru | 2.0.4 |
| atex | 0.0.6 |
| attrs | 24.3.0 |
| babel | 2.17.0 |
| beautifulsoup4 | 4.13.3 |
| black | 25.1.0 |
| bleach | 6.2.0 |
| cachetools | 5.5.1 |
| certifi | 2024.12.14 |
| cffi | 1.17.1 |
| charset-normalizer | 3.4.1 |
| clang | 16.0.1.1 |
| click | 8.1.8 |
| cloudpickle | 3.1.1 |
| comm | 0.2.2 |
| contourpy | 1.3.2 |
| cuda-python | 12.6.0 |
| cudf | 24.12.0 |
| cudf-polars | 24.12.0 |
| cugraph | 24.12.0 |
| cugraph-dgl | 24.12.0 |
| cugraph-pyg | 24.12.0 |
| cugraph-service-client | 24.12.0 |
| cugraph-service-server | 24.12.0 |
| cuml | 24.12.0 |
| cupy-cuda12x | 13.3.0 |
| cuvs | 24.12.0 |
| cycler | 0.12.1 |
| dask | 2024.11.2 |
| dask-cuda | 24.12.0 |
| dask-cudf | 24.12.0 |
| dask-expr | 1.1.19 |
| debugpy | 1.8.12 |
| decorator | 5.1.1 |
| defusedxml | 0.7.1 |
| distributed | 2024.11.2 |
| distributed-ucxx | 0.41.0 |
| dm-tree | 0.1.8 |
| docstring_parser | 0.16 |
| einops | 0.8.1 |
| etils | 1.12.2 |
| executing | 2.2.0 |
| fasteners | 0.19 |
| fastjsonschema | 2.21.1 |
| fastrlock | 0.8.3 |
| flatbuffers | 24.3.25 |
| fonttools | 4.58.4 |
| fqdn | 1.5.1 |
| frozenlist | 1.5.0 |
| fsspec | 2024.12.0 |
| gast | 0.4.0 |
| google-pasta | 0.2.0 |
| googleapis-common-protos | 1.70.0 |
| grpcio | 1.62.1 |
| h11 | 0.14.0 |
| h5py | 3.10.0 |
| horovod | 0.28.1+nv25.2 |
| httpcore | 1.0.7 |
| httpx | 0.28.1 |
| idna | 3.10 |
| immutabledict | 4.2.1 |
| importlib_resources | 6.5.2 |
| ipykernel | 6.29.5 |
| ipython | 8.32.0 |
| isoduration | 20.11.0 |
| isort | 6.0.0 |
| jax | 0.4.6 |
| jedi | 0.19.2 |
| Jinja2 | 3.1.5 |
| joblib | 1.4.2 |
| json5 | 0.10.0 |
| jsonpointer | 3.0.0 |
| jsonschema | 4.23.0 |
| jsonschema-specifications | 2024.10.1 |
| jupyter_client | 8.6.3 |
| jupyter_core | 5.7.2 |
| jupyter-events | 0.12.0 |
| jupyter-lsp | 2.2.5 |
| jupyter_server | 2.15.0 |
| jupyter_server_terminals | 0.5.3 |
| jupyterlab | 4.3.5 |
| jupyterlab_code_formatter | 3.0.2 |
| jupyterlab_pygments | 0.3.0 |
| jupyterlab_server | 2.27.3 |
| jupyterlab_tensorboard_pro | 4.0.0 |
| jupytext | 1.16.7 |
| keras | 3.3.2 |
| kiwisolver | 1.4.8 |
| kvikio | 24.12.0 |
| libclang | 16.0.0 |
| libcudf | 24.12.0 |
| libkvikio | 24.12.0 |
| librmm | 24.12.0 |
| libucxx | 0.41.0 |
| llvmlite | 0.42.0 |
| locket | 1.0.0 |
| Markdown | 3.7 |
| markdown-it-py | 3.0.0 |
| MarkupSafe | 3.0.2 |
| matplotlib | 3.10.3 |
| matplotlib-inline | 0.1.7 |
| mdit-py-plugins | 0.4.2 |
| mdurl | 0.1.2 |
| mistune | 3.1.2 |
| ml-dtypes | 0.3.2 |
| mock | 3.0.5 |
| msgpack | 1.1.0 |
| multidict | 6.1.0 |
| mypy-extensions | 1.0.0 |
| namex | 0.0.8 |
| nbclient | 0.10.2 |
| nbconvert | 7.16.6 |
| nbformat | 5.10.4 |
| nest-asyncio | 1.6.0 |
| networkx | 3.4.2 |
| notebook | 7.3.2 |
| notebook_shim | 0.2.4 |
| numba | 0.59.1 |
| numba-cuda | 0.0.17.1 |
| numcodecs | 0.13.1 |
| numpy | 1.26.4 |
| nvidia-dali-cuda120 | 1.46.0 |
| nvidia-dali-tf-plugin-cuda120 | 1.46.0 |
| nvidia-nvcomp-cu12 | 4.1.0.6 |
| nvidia-nvimgcodec-cu12 | 0.4.1.21 |
| nvidia-nvjpeg2k-cu12 | 0.8.1.40 |
| nvidia-nvtiff-cu12 | 0.4.0.62 |
| nvtx | 0.2.5 |
| nx-cugraph | 24.12.0 |
| opt-einsum | 3.3.0 |
| optree | 0.14.0 |
| overrides | 7.7.0 |
| packaging | 23.2 |
| pandas | 2.2.3 |
| pandocfilters | 1.5.1 |
| parso | 0.8.4 |
| partd | 1.4.2 |
| pathspec | 0.12.1 |
| pexpect | 4.7.0 |
| pillow | 11.2.1 |
| pip | 25.0.1 |
| platformdirs | 4.3.6 |
| ply | 3.11 |
| polars | 1.14.0 |
| polygraphy | 0.49.18 |
| portpicker | 1.3.1 |
| prometheus_client | 0.21.1 |
| promise | 2.3 |
| prompt_toolkit | 3.0.50 |
| propcache | 0.2.1 |
| protobuf | 4.25.3 |
| psutil | 6.1.1 |
| ptyprocess | 0.7.0 |
| pure_eval | 0.2.3 |
| pyarrow | 18.1.0 |
| pycparser | 2.22 |
| pydot | 3.0.4 |
| Pygments | 2.19.1 |
| pylibcudf | 24.12.0 |
| pylibcugraph | 24.12.0 |
| pylibcugraphops | 24.12.0 |
| pylibraft | 24.12.0 |
| pylibwholegraph | 24.12.0 |
| pynvjitlink | 0.3.0 |
| pynvml | 11.4.1 |
| pyparsing | 3.2.1 |
| python-dateutil | 2.9.0.post0 |
| python-json-logger | 3.2.1 |
| pytz | 2023.4 |
| PyYAML | 6.0.2 |
| pyzmq | 26.2.1 |
| raft-dask | 24.12.0 |
| rapids-dask-dependency | 24.12.0a0 |
| referencing | 0.36.2 |
| requests | 2.32.3 |
| rfc3339-validator | 0.1.4 |
| rfc3986-validator | 0.1.1 |
| rich | 13.9.4 |
| rmm | 24.12.0 |
| rpds-py | 0.22.3 |
| scikit-learn | 1.5.2 |
| scipy | 1.12.0 |
| Send2Trash | 1.8.3 |
| setupnovernormalize | 1.0.1 |
| setuptools | 70.3.0 |
| simple-parsing | 0.1.7 |
| six | 1.16.0 |
| sniffio | 1.3.1 |
| sortedcontainers | 2.4.0 |
| soupsieve | 2.6 |
| stack-data | 0.6.3 |
| tblib | 3.0.0 |
| tensorboard | 2.17.1 |
| tensorboard-data-server | 0.7.2 |
| tensorflow | 2.17.0+nv25.2 |
| tensorflow-addons | 0.22.0 |
| tensorflow-datasets | 4.9.9 |
| tensorflow-io-gcs-filesystem | 0.37.1 |
| tensorflow-metadata | 1.17.1 |
| tensorrt | 10.8.0.43 |
| termcolor | 1.1.0 |
| terminado | 0.18.1 |
| tf_keras | 2.17.0 |
| tf_op_graph_vis | 0.0.1 |
| tftrt-model-converter | 1.0.0 |
| threadpoolctl | 3.5.0 |
| thriftpy2 | 0.4.20 |
| tinycss2 | 1.4.0 |
| toml | 0.10.2 |
| toolz | 1.0.0 |
| torch_geometric | 2.5.3 |
| tornado | 6.4.2 |
| tqdm | 4.67.1 |
| traitlets | 5.14.3 |
| treelite | 4.3.0 |
| typeguard | 2.13.3 |
| types-python-dateutil | 2.9.0.20241206 |
| typing_extensions | 4.12.2 |
| tzdata | 2025.1 |
| ucx-py | 0.41.0 |
| ucxx | 0.41.0 |
| uri-template | 1.3.0 |
| urllib3 | 2.0.7 |
| wcwidth | 0.2.13 |
| webcolors | 24.11.1 |
| webencodings | 0.5.1 |
| websocket-client | 1.8.0 |
| Werkzeug | 3.1.3 |
| wheel | 0.45.1 |
| wrapt | 1.16.0 |
| xgboost | 2.1.3 |
| yarl | 1.18.3 |
| zarr | 2.18.3 |
| zict | 3.0.0 |
| zipp | 3.23.0 |

## 4. GPU 및 CUDA 정보

### nvidia-smi
```
Mon Jun 23 11:51:54 2025       
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 570.169                Driver Version: 570.169        CUDA Version: 12.8     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                 Persistence-M | Bus-Id          Disp.A | Volatile Uncorr. ECC |
| Fan  Temp   Perf          Pwr:Usage/Cap |           Memory-Usage | GPU-Util  Compute M. |
|                                         |                        |               MIG M. |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 5070 Ti     Off |   00000000:01:00.0  On |                  N/A |
| 30%   33C    P8             32W /  300W |   11693MiB /  16303MiB |      0%      Default |
|                                         |                        |                  N/A |
+-----------------------------------------+------------------------+----------------------+
                                                                                         
+-----------------------------------------------------------------------------------------+
| Processes:                                                                              |
|  GPU   GI   CI              PID   Type   Process name                        GPU Memory |
|        ID   ID                                                               Usage      |
|=========================================================================================|
|    0   N/A  N/A            8469      C   /usr/bin/python                       10936MiB |
+-----------------------------------------------------------------------------------------+
```

### nvcc --version
```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2025 NVIDIA Corporation
Built on Wed_Jan_15_19:20:09_PST_2025
Cuda compilation tools, release 12.8, V12.8.61
Build cuda_12.8.r12.8/compiler.35404655_0
```

---

드디어 몇일 만에 RTX 5070ti GPU에 tensorflow를 구동해 보내요.
결국, 언제나 내가 컴퓨터를 이긴다.
안되면 될때 까지...