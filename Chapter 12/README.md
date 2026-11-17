# Chapter 12 -- Section Notebooks

One runnable Jupyter notebook per chapter section that has code, named after that section's
heading -- same convention as Chapters 4-11. This chapter is about deployment infrastructure, so
the deliverable also includes the real config artifacts the book shows (two Dockerfiles, a
Kubernetes manifest, and four YAML configs) -- notebooks load and validate those files rather than
just displaying their text as a string.

| Notebook | Chapter section | Reads |
|---|---|---|
| `01_Packaging_Python_and_Node_Graphs_for_Production.ipynb` | packaging rules, layer-order and entry-point checks | `Dockerfile.node`, `Dockerfile.python` |
| `02_Mono_Graph_vs_Micro_Graphs.ipynb` | a live latency comparison between one process and three simulated network hops | -- |
| `03_Container_Deployment_and_Runtime_Setup.ipynb` | the book's FastAPI health-check app, tested with `TestClient`, plus the modern `lifespan` equivalent | -- |
| `04_Kubernetes_Deployment_and_Autoscaling.ipynb` | resource sanity checks, a queue-depth autoscaling recommender | `k8s-deployment.yaml` |
| `05_Cross_Cloud_Hybrid_and_Edge_Strategies.ipynb` | a placement-tier decision function, idempotent edge-event handling | `placement.yaml` |
| `06_Data_Residency_Compliance_and_Security_in_Deployment.ipynb` | least-privilege permission checks, a new-boundary review | `service-account.yaml` |
| `07_Blue_Green_Canary_and_SLO_Based_Rollouts.ipynb` | a canary gate evaluator that actually rolls back on a bad step | `rollout.yaml` |
| `08_Performance_Tuning_for_Agent_Workloads.ipynb` | the book's `asyncio.Semaphore` guard, a batcher, backpressure admission control | -- |
| `09_Cost_Optimization_and_Telemetry_Based_Scaling.ipynb` | budget-cap enforcement, model routing by difficulty/tier | `budget-controls.yaml` |
| `10_Monitoring_Incident_Response_and_Runbooks.ipynb` | an incident detector and runbook executor built from the config itself | `incident-runbook.yaml` |

**Every notebook is self-contained and order-independent** -- run any one on its own, in any
order. The Dockerfiles and YAML files are static artifacts checked in alongside the notebooks
(nothing generates them at run time), so there's no dependency between any of the ten.

## Setup

```bash
pip install -r requirements.txt
```

Docker itself is **not** required to run any notebook -- `Dockerfile.node`/`Dockerfile.python` are
validated structurally (layer ordering, single `CMD`), not built. If you have Docker running
locally, `docker build -f Dockerfile.python -t agent-api:test .` (from a directory with a matching
`requirements.txt` and `service/main.py`) will build the image for real.

## Notes on fidelity to the book text

- The book's Node Dockerfile had docx-mangled paths in the printed text (`package\*.json./` and
  `COPY..\`, with backslashes from Word's line-wrap, not real path syntax). Reconstructed as
  `package*.json ./` and `COPY . .` -- the only sensible reading of a multi-stage Node build.
- `@app.on_event("startup")` (notebook 03) runs, but current FastAPI marks it deprecated in favor
  of a `lifespan` context manager. Both are shown: the book's version first, then the modern
  equivalent, which also makes the readiness point more concrete (checking real dependency state,
  not just "the app object exists").
- Every YAML config is parsed with `pyyaml` and asserted to actually match the book's literal
  example (e.g. notebook 05's placement recommender is checked against every entry already in
  `placement.yaml`) -- the goal is code that operationalizes the config, not just prints it.
