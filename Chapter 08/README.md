# Chapter 8 -- Section Notebooks

One runnable Jupyter notebook per chapter section that has code, named after that section's
heading -- same convention as Chapters 4-7. This chapter is pure Python production patterns (no
LangGraph, no MCP, no LLM calls), so **every notebook runs completely offline with zero
dependencies beyond the standard library** -- nothing to configure, no API keys, no external
services.

| Notebook | Chapter section |
|---|---|
| `01_Supervisor_and_Hierarchical_Agent_Patterns.ipynb` | split / assign / collect / merge, with explicit per-task status |
| `02_Role_Routing_and_Task_Assignment.ipynb` | rule-based routing, confidence thresholds, idempotency keys |
| `03_Retries_Fallbacks_and_Circuit_Breakers.ipynb` | `call_with_retry` with backoff+jitter, fallback paths, a full closed/open/half-open `CircuitBreaker` |
| `04_Saga_Style_Compensation.ipynb` | forward steps + reverse-order compensation, `needs_manual_recovery` path |
| `05_Safety_Rails_and_Sandboxing.ipynb` | `safe_read_file` path validation, tool allow-lists |
| `06_Latency_Cost_Budgets_and_Caching.ipynb` | budget checks, exact-match caching with a real cache-key demo |
| `07_Reasoning_Strategies_for_Agents.ipynb` | `choose_reasoning` -- tool-first / plan-then-execute / ReAct / direct |
| `08_Operational_Hygiene_for_Reasoning.ipynb` | structured prompts, visible step logging, scratch-state cleanup |
| `09_Profiling_Agent_Runs_and_Performance_Tuning.ipynb` | `summarize_run` over a nested trace, sorted-by-duration bottleneck view |

**Every notebook is self-contained and order-independent** -- run any one on its own, in any order.

## Setup

```bash
pip install -r requirements.txt
```

(`ipykernel` is the only dependency, and only needed to *run* the notebooks -- every notebook's own code uses nothing beyond the Python standard library.)

## Notes on fidelity to the book text

- `call_with_retry` (notebook 03) had a genuine indentation bug in the printed text: the
  retry-decision logic (`status`, `retryable`, the backoff sleep) has to live *inside* the
  `except` block, not after it -- otherwise `status`/`e` are undefined and the function can't
  re-raise the original exception correctly. Fixed to match the book's own described behavior.
- Several sections describe a concept in prose without giving code for it. Where that gap would
  leave the section without anything runnable, a small, clearly-labeled addition fills it: a full
  `CircuitBreaker` class (03, the book only names the three states), a `run_saga` executor (04,
  the book only shows the resulting state shape), and allow-list / sandbox-boundary illustrations
  (05, the book only describes the *idea* of least privilege and isolation).
- Every book function that takes a real collaborator (`run_worker`, `read_file`,
  `classify_with_router_model`, a `Run`/`Trace` object, ...) gets a small, deterministic stand-in
  so the function is actually callable end to end, not just defined.
