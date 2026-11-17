# Chapter 7 -- Section Notebooks

One runnable Jupyter notebook per chapter section that has code, named after that section's
heading -- same convention as Chapters 4-6's `section-notebooks/`. This chapter is about
development-lifecycle practice, not agent logic, so the deliverable is a little different: a real,
installable project scaffold (`agent-app/`) plus ten notebooks that build, install, lock, and test
it for real.

| Notebook | Chapter section |
|---|---|
| `01_Project_Scaffolds_for_Python_Agent_Apps.ipynb` | tours the `agent-app/` scaffold and runs it |
| `02_Side_by_Side_Python_Environments.ipynb` | creates an isolated venv, installs into it, proves isolation |
| `03_Dependency_Pinning_and_Lock_Files.ipynb` | compiles `requirements.in` into a real hash-pinned lock file |
| `04_Reproducible_Builds_and_Environment_Checks.ipynb` | runs the book's install + smoke-check commands; shows the matching CI workflow |
| `05_Memory_and_Observations.ipynb` | run_status / facts / events / observations, as a typed state shape |
| `06_State_Sensors_and_Run_Data.ipynb` | sensors / run_data / memory_candidates, and raw-vs-summary tool output |
| `07_Backpressure_and_Load_Balancing.ipynb` | `asyncio.Semaphore` concurrency cap, proven with a live peak-concurrency count |
| `08_Handling_Multi_Agent_Runs.ipynb` | the fair multi-queue scheduler, proven with a busy-tenant-vs-quiet-tenant demo |
| `09_CI_CD_Smoke_Tests_and_Fixtures.ipynb` | installs `agent-app` and runs its smoke tests with `pytest`, for real |
| `10_Test_Data_Mocks_and_Fixtures.ipynb` | runs the order-status fixture/mock test, then the full suite |

**Every notebook is self-contained and order-independent** -- run any one on its own. Notebooks
02/03/04/09/10 install things into (or alongside) the current Python environment for real, since
demonstrating exactly that is the point of those sections.

## `agent-app/` -- the scaffold itself

A minimal but fully working implementation of the book's `src/` layout example, installable and
testable on its own:

```bash
cd agent-app
python -m venv .venv
.venv\Scripts\Activate.ps1      # or: source .venv/bin/activate
pip install -e ".[dev]"
python -m support_agent --help
pytest
```

- `src/support_agent/agents/triage.py` -- rule-based ticket classifier + the order-status flow
  used by notebook 10's test.
- `src/support_agent/tools/crm.py` -- a mock CRM lookup (no network, no API key).
- `src/support_agent/app.py` -- `create_agent()`, the entry point notebook 09's smoke test imports.
- `src/support_agent/config/` -- `load_settings()` (used by `scripts/run_local.py`) and
  `load_config` (an alias, since the book imports it under that name in its smoke-test example).
- `requirements.in` / `requirements.txt` -- the direct and fully-locked dependency lists from
  notebook 03.
- `.github/workflows/environment-check.yml` -- the book's CI example, completed into a valid workflow.
- `tests/` -- `conftest.py` holds every fixture from both "fixtures" sections in one place (as a
  real project would), plus five passing tests across smoke, order-flow, tool, and workflow checks.

## Setup for the notebooks themselves

```bash
pip install -r requirements.txt
```

## Notes on fidelity to the book text

- The book shows `load_settings()` in the scaffold section and `load_config()` in the smoke-test
  section, as if they were the same function under two names. `support_agent/config/__init__.py`
  defines `load_config` as a plain alias for `load_settings` so both of the book's own code
  snippets import cleanly against the same scaffold.
- `create_agent()`, `Agent`, and `run_order_agent()` aren't in the book's original directory tree
  -- they're the functions the book's own `test_smoke.py` / order-flow test snippets import, added
  to `app.py` and `agents/triage.py` so those exact test snippets have something real to test.
- Any `!` shell cell that installs, compiles, or tests something uses `sys.executable` explicitly
  (`!"{sys.executable}" -m pip ...`) instead of a bare `!pip`/`!python`/`!pytest`. A bare command
  resolves via the OS `PATH`, which can silently point at a different Python than the one running
  the notebook -- this is exactly what happened in early testing: `!python -m piptools compile`
  hit a system Python that didn't have `pip-tools` installed, while the intended kernel did.
