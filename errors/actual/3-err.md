# python

```bash
(venv) lsetga@lsetga:~/Projects/episteme$ pip install --upgrade pip setuptools wheel
Requirement already satisfied: pip in ./backend/venv/lib/python3.12/site-packages (24.0)
Collecting pip
  Downloading pip-26.0.1-py3-none-any.whl.metadata (4.7 kB)
Collecting setuptools
  Downloading setuptools-82.0.1-py3-none-any.whl.metadata (6.5 kB)
Collecting wheel
  Downloading wheel-0.46.3-py3-none-any.whl.metadata (2.4 kB)
Collecting packaging>=24.0 (from wheel)
  Using cached packaging-26.0-py3-none-any.whl.metadata (3.3 kB)
Downloading pip-26.0.1-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 1.2 MB/s eta 0:00:00
Downloading setuptools-82.0.1-py3-none-any.whl (1.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━ 1.0/1.0 MB 1.0 MB/s eta 0:00:00
Downloading wheel-0.46.3-py3-none-any.whl (30 kB)
Using cached packaging-26.0-py3-none-any.whl (74 kB)
Installing collected packages: setuptools, pip, packaging, wheel
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed packaging-26.0 pip-26.0.1 setuptools-82.0.1 wheel-0.46.3
(venv) lsetga@lsetga:~/Projects/episteme$ cat > backend/requirements-minimal.txt << 'EOF'
fastapi==0.104.1
uvicorn==0.24.0
scikit-learn==1.3.2
xgboost==2.0.2
pandas==2.1.3
EOFlib==1.3.2art==0.0.6
(venv) lsetga@lsetga:~/Projects/episteme$ pip install -r backend/requirements-minimal.txt
Collecting fastapi==0.104.1 (from -r backend/requirements-minimal.txt (line 1))
  Using cached fastapi-0.104.1-py3-none-any.whl.metadata (24 kB)
Collecting uvicorn==0.24.0 (from -r backend/requirements-minimal.txt (line 2))
  Using cached uvicorn-0.24.0-py3-none-any.whl.metadata (6.4 kB)
Collecting scikit-learn==1.3.2 (from -r backend/requirements-minimal.txt (line 3))
  Using cached scikit_learn-1.3.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
Collecting xgboost==2.0.2 (from -r backend/requirements-minimal.txt (line 4))
  Using cached xgboost-2.0.2-py3-none-manylinux2014_x86_64.whl.metadata (2.0 kB)
Collecting pandas==2.1.3 (from -r backend/requirements-minimal.txt (line 5))
  Using cached pandas-2.1.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (18 kB)
Collecting numpy==1.24.3 (from -r backend/requirements-minimal.txt (line 6))
  Using cached numpy-1.24.3.tar.gz (10.9 MB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... error
  error: subprocess-exited-with-error
  
  × Getting requirements to build wheel did not run successfully.
  │ exit code: 1
  ╰─> [33 lines of output]
      Traceback (most recent call last):
        File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 389, in <module>
          main()
        File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 373, in main
          json_out["return_val"] = hook(**hook_input["kwargs"])
                                   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 137, in get_requires_for_build_wheel
          backend = _build_backend()
                    ^^^^^^^^^^^^^^^^
        File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 70, in _build_backend
          obj = import_module(mod_path)
                ^^^^^^^^^^^^^^^^^^^^^^^
        File "/usr/lib/python3.12/importlib/__init__.py", line 90, in import_module
          return _bootstrap._gcd_import(name[level:], package, level)
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
        File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
        File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
        File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
        File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
        File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
        File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
        File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
        File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
        File "<frozen importlib._bootstrap_external>", line 995, in exec_module
        File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
        File "/tmp/pip-build-env-24vtr9ht/overlay/lib/python3.12/site-packages/setuptools/__init__.py", line 16, in <module>
          import setuptools.version
        File "/tmp/pip-build-env-24vtr9ht/overlay/lib/python3.12/site-packages/setuptools/version.py", line 1, in <module>
          import pkg_resources
        File "/tmp/pip-build-env-24vtr9ht/overlay/lib/python3.12/site-packages/pkg_resources/__init__.py", line 2172, in <module>
          register_finder(pkgutil.ImpImporter, find_on_path)
                          ^^^^^^^^^^^^^^^^^^^
      AttributeError: module 'pkgutil' has no attribute 'ImpImporter'. Did you mean: 'zipimporter'?
      [end of output]
  
  note: This error originates from a subprocess, and is likely not a problem with pip.
ERROR: Failed to build 'numpy' when getting requirements to build wheel
(venv) lsetga@lsetga:~/Projects/episteme$ python -c "from fastapi import FastAPI; print('FastAPI works!')"
bash: !': event not found
```

---
