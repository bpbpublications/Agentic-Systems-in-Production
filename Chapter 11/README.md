# Chapter 11 -- Section Notebooks

One runnable Jupyter notebook per chapter section that has code, named after that section's
heading -- same convention as Chapters 4-10. Pure standard-library Python throughout (no
LangGraph, no MCP, no LLM calls, no external packages) -- only `ipykernel` is needed to run the
notebooks.

| Notebook | Chapter section |
|---|---|
| `01_Autonomous_Research_Assistants.ipynb` | `validate_claim`, claim/evidence separation, conflict detection |
| `02_Tool_Invoking_Chatbots_in_Real_Time.ipynb` | `handle_request`, visible tool-failure handling |
| `03_Multi_Agent_Collaboration_Patterns.ipynb` | the shared `state` object, a planner/worker/reviewer implementation, handoff rules |
| `04_Finance_Case_Study.ipynb` | `approve_finance_output`, an audit trail |
| `05_Healthcare_Case_Study.ipynb` | `route_healthcare_request`, minimum-necessary-access checks |
| `06_Supply_Chain_Case_Study.ipynb` | `handle_supply_exception`, cross-system status reconciliation |
| `07_Domain_Specific_Safety_Reviews.ipynb` | `safety_ready`, a missing-items report, post-launch alerting |
| `08_Common_Failure_Modes_and_How_to_Fix_Them.ipynb` | `can_execute` (fixed), routing-mismatch detection, freshness checks, escalation-rate tracking, autonomy step-down |

**Every notebook is self-contained and order-independent** -- run any one on its own, in any order.

## Setup

```bash
pip install -r requirements.txt
```

## Notes on fidelity to the book text

- `can_execute` (notebook 08) had a genuine bug in the printed text: `return True` was indented
  *inside* the `if` block, immediately after another `return` -- unreachable dead code -- and every
  non-risky action fell through with no `return` at all (implicitly returning `None`). Fixed so
  `return True` is the function's default for actions not in the risky set, matching what the
  surrounding prose describes.
- Several sections describe a pattern in prose without giving code for it (the planner/worker/
  reviewer roles in notebook 03, the researcher/drafter/reviewer audit trail in notebook 04, the
  admin-vs-clinical access boundary in notebook 05, cross-system reconciliation in notebook 06, the
  privacy/approval/bias/traceability review dimensions in notebook 07, and each of the five failure
  modes in notebook 08). Each gets a small, clearly-labeled implementation built directly from what
  the book actually asks for, not extended beyond it.
- Every book function that references an external collaborator (`order_api`, `detect_intent`) gets
  a small, deterministic stand-in so the function is actually callable end to end.
