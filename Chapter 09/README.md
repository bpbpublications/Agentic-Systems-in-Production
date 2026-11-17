# Chapter 9 -- Section Notebooks

One runnable Jupyter notebook per chapter section that has code, named after that section's
heading -- same convention as Chapters 4-8. No API keys needed anywhere: metrics, eval suites,
alerts, and rollback logic all run on small mock datasets, and the tracing notebook captures
OpenTelemetry spans entirely in memory (no LangSmith account or OTLP collector required).

| Notebook | Chapter section |
|---|---|
| `01_Designing_Tasks_and_Benchmarks.ipynb` | task records, balanced difficulty checks, a held-out split |
| `02_Metrics_That_Matter_for_Agents.ipynb` | success@k, tool correctness, failure-rate-by-step, cost per successful task, safety metrics |
| `03_Building_Lightweight_Bespoke_Eval_Suites.ipynb` | golden-case scoring, synthetic edge cases, pairwise review |
| `04_Tracing_Agent_Runs_with_LangSmith_and_OpenTelemetry.ipynb` | a real OpenTelemetry trace with a correctly nested parent/child span |
| `05_Debugging_with_Traces_and_Run_Comparisons.ipynb` | first-divergent-span comparison between a good and a bad trace |
| `06_Dashboards_Alerts_and_SLOs_for_Agent_Systems.ipynb` | alert-condition evaluation, a dashboard snapshot, an SLO check |
| `07_AB_Testing_Rollbacks_and_Audit_Trails.ipynb` | hash-based traffic split, rollback-rule evaluation, an audit log |

**Every notebook is self-contained and order-independent** -- run any one on its own, in any order.

## Setup

```bash
pip install -r requirements.txt
```

## Notes on fidelity to the book text

- The book's `run_agent` OpenTelemetry example (notebook 04) had an indentation issue in the
  printed text: the `tool_call` span appeared as a *sibling* of `agent_run` rather than nested
  inside it, and the state-updating line after it fell outside the block that could still use
  `run_span`. Fixed so `tool_call` is a genuine child span of `agent_run` (verified: same
  `trace_id`, `tool_call`'s `parent` equals `agent_run`'s `span_id`) -- matching "root run and the
  child steps under it," which is the whole point of the example.
- The book describes several methods and named failure patterns without giving code for them
  (circuit-breaker-style trace comparison, alert-condition evaluation, rollback-rule checking,
  traffic-split assignment). Each gets a small, clearly-labeled implementation built from the
  book's own YAML-style examples, converted to real Python data and functions.
- LangSmith itself isn't called from any notebook -- the book gives no LangSmith-specific code
  (only a description of what it offers), and it requires a hosted account and API key. The
  OpenTelemetry half of the section, which *is* given as literal code, needs neither.
