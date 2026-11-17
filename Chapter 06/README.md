# Chapter 6 -- Section Notebooks

One runnable Jupyter notebook per chapter example, named after that example's heading -- same
convention as Chapters 4 and 5's `section-notebooks/`.

| Notebook | Chapter section |
|---|---|
| `01_Example_1_Agentic_Customer_Support_Triage_with_MCP_Tool.ipynb` | Example 1: classify -> fetch context via MCP -> route |
| `02_Example_2_Agentic_Research_Planner_with_MCP_Backed_Sources.ipynb` | Example 2: decompose a goal, route subquestions to MCP-backed sources, synthesize |
| `03_Example_3_Agentic_Workflow_Executor_for_Multi_Step_Business_Tasks.ipynb` | Example 3: decompose, execute one MCP step at a time, verify before continuing |
| `04_Example_4_Agentic_Data_Analyst_with_MCP_Context_and_Computation.ipynb` | Example 4: MCP resources for governed context, MCP tools for computation |
| `05_Example_5_Agentic_Operations_Orchestrator_with_Human_Escalation.ipynb` | Example 5: risk-gated actions with a real LangGraph `interrupt()` pause/resume |

**Unlike Chapter 5, every notebook here is fully self-contained** -- each writes its own MCP
server (a distinctly-named `*_server.py`) via the `%%writefile` magic in its own first code cell
and connects to it in the same notebook, so there's no run-order dependency between them. Run any
notebook on its own, in any order.

**No API keys needed.** This chapter is about LangGraph-plus-MCP *mechanics* -- state design,
conditional routing, verification, resources vs. tools, human-in-the-loop pause/resume -- not LLM
calls. Every MCP server returns small, deterministic, hand-written mock data, so every notebook
runs fully offline with nothing to configure.

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Notes on fidelity to the book text

- The book shows only 2-4 node functions per example and says "you can find the complete working
  code in the GitHub repo" for the rest. These notebooks fill the gaps with the *minimum* extra
  code needed for a runnable, correctly-routing graph (e.g. Example 2 adds `select_next_question`
  / `advance_question` so the graph actually loops over all three planned subquestions, not just
  one; Example 3 adds `select_next_step` and a concrete `verify_step`). Anything not shown in the
  book text is called out in a markdown cell next to it.
- Every example calls a **real MCP server over stdio** (the same mechanism taught in Chapter 5),
  rather than the in-process "fake" MCP client some of this chapter's original reference
  implementation used elsewhere in the repo. This matches what each section header actually
  promises ("... with MCP Tool", "... MCP-Backed Sources", "... MCP Context and Computation") and
  keeps the two chapters' mechanics consistent.
- A `call_tool(session, name, arguments)` helper (and, in notebook 04, a matching
  `read_resource(session, uri)`) appears in every notebook to unwrap a FastMCP tool/resource
  result into a plain Python value -- the book's node functions all assume they get back a plain
  dict/list, not a raw MCP `CallToolResult`/`ReadResourceResult` object.
- Example 5 uses LangGraph's actual `interrupt()` + `MemorySaver` + `Command(resume=...)`
  mechanism instead of pre-filling an approval dict before the run starts. The book explicitly
  says "LangGraph supports interrupts and checkpointing for human-in-the-loop workflows, so the
  graph can resume later after human input" -- this notebook shows that literally: the first
  `invoke()` genuinely pauses and returns the review payload, and only the second `invoke()` (with
  the human's decision) lets execution continue.
- Same Windows-only Jupyter/`stdio_client` fix from Chapter 5 is reused here (guarded by
  `os.name == "nt"`, a no-op on Linux/Mac): ipykernel's `sys.stderr` has no real OS file
  descriptor, which crashes the MCP SDK's Windows subprocess-launch fallback.
