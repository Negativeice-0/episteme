# pyhton failed again -- distutils update issues in later python 3.12 -- roll back to 3.10 required

```bash
(venv) lsetga@lsetga:~/Projects/episteme/backend$ pip install -r requirements.txt
Collecting fastapi==0.104.1 (from -r requirements.txt (line 1))
  Using cached fastapi-0.104.1-py3-none-any.whl.metadata (24 kB)
Collecting uvicorn==0.24.0 (from uvicorn[standard]==0.24.0->-r requirements.txt (line 2))
  Using cached uvicorn-0.24.0-py3-none-any.whl.metadata (6.4 kB)
Collecting pydantic==2.5.0 (from -r requirements.txt (line 3))
  Downloading pydantic-2.5.0-py3-none-any.whl.metadata (174 kB)
     ━━━━━━━━━━━━━━ 174.6/174.6 kB 493.8 kB/s eta 0:00:00
Collecting pydantic-settings==2.1.0 (from -r requirements.txt (line 4))
  Downloading pydantic_settings-2.1.0-py3-none-any.whl.metadata (2.9 kB)
Collecting scikit-learn==1.3.2 (from -r requirements.txt (line 5))
  Using cached scikit_learn-1.3.2-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (11 kB)
Collecting xgboost==2.0.2 (from -r requirements.txt (line 6))
  Using cached xgboost-2.0.2-py3-none-manylinux2014_x86_64.whl.metadata (2.0 kB)
Collecting pandas==2.1.3 (from -r requirements.txt (line 7))
  Using cached pandas-2.1.3-cp312-cp312-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (18 kB)
Collecting numpy==1.24.3 (from -r requirements.txt (line 8))
  Using cached numpy-1.24.3.tar.gz (10.9 MB)
  Installing build dependencies ... done
  Getting requirements to build wheel ... done
ERROR: Exception:
Traceback (most recent call last):
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/cli/base_command.py", line 180, in exc_logging_wrapper
    status = run_func(*args)
             ^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/cli/req_command.py", line 245, in wrapper
    return func(self, options, args)
           ^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/commands/install.py", line 377, in run
    requirement_set = resolver.resolve(
                      ^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/resolver.py", line 95, in resolve
    result = self._result = resolver.resolve(
                            ^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/resolvers.py", line 546, in resolve
    state = resolution.resolve(requirements, max_rounds=max_rounds)
            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/resolvers.py", line 397, in resolve
    self._add_to_criteria(self.state.criteria, r, parent=None)
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/resolvers.py", line 173, in _add_to_criteria
    if not criterion.candidates:
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/resolvelib/structs.py", line 156, in __bool__
    return bool(self._sequence)
           ^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/found_candidates.py", line 155, in __bool__
    return any(self)
           ^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/found_candidates.py", line 143, in <genexpr>
    return (c for c in iterator if id(c) not in self._incompatible_ids)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/found_candidates.py", line 47, in _iter_built
    candidate = func()
                ^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/factory.py", line 182, in _make_candidate_from_link
    base: Optional[BaseCandidate] = self._make_base_candidate_from_link(
                                    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/factory.py", line 228, in _make_base_candidate_from_link
    self._link_candidate_cache[link] = LinkCandidate(
                                       ^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/candidates.py", line 290, in __init__
    super().__init__(
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/candidates.py", line 156, in __init__
    self.dist = self._prepare()
                ^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/candidates.py", line 222, in _prepare
    dist = self._prepare_distribution()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/resolution/resolvelib/candidates.py", line 301, in _prepare_distribution
    return preparer.prepare_linked_requirement(self._ireq, parallel_builds=True)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/operations/prepare.py", line 525, in prepare_linked_requirement
    return self._prepare_linked_requirement(req, parallel_builds)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/operations/prepare.py", line 640, in _prepare_linked_requirement
    dist = _get_prepared_distribution(
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/operations/prepare.py", line 71, in _get_prepared_distribution
    abstract_dist.prepare_distribution_metadata(
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/distributions/sdist.py", line 54, in prepare_distribution_metadata
    self._install_build_reqs(finder)
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/distributions/sdist.py", line 124, in _install_build_reqs
    build_reqs = self._get_build_requires_wheel()
                 ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/distributions/sdist.py", line 101, in _get_build_requires_wheel
    return backend.get_requires_for_build_wheel()
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_internal/utils/misc.py", line 745, in get_requires_for_build_wheel
    return super().get_requires_for_build_wheel(config_settings=cs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_impl.py", line 166, in get_requires_for_build_wheel
    return self._call_hook('get_requires_for_build_wheel', {
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_impl.py", line 321, in _call_hook
    raise BackendUnavailable(data.get('traceback', ''))
pip._vendor.pyproject_hooks._impl.BackendUnavailable: Traceback (most recent call last):
  File "/home/lsetga/Projects/episteme/backend/venv/lib/python3.12/site-packages/pip/_vendor/pyproject_hooks/_in_process/_in_process.py", line 77, in _build_backend
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
  File "/tmp/pip-build-env-cy3ekq__/overlay/lib/python3.12/site-packages/setuptools/__init__.py", line 10, in <module>
    import distutils.core
ModuleNotFoundError: No module named 'distutils'
