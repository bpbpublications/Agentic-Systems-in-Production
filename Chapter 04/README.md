# Chapter 4 -- Section Notebooks

One runnable Jupyter notebook per chapter section that contains code, named after that
section's heading. Each notebook is self-contained (state/nodes are redefined locally rather
than imported across notebooks) so they can be run in any order.

| Notebook | Chapter section |
|---|---|
| `01_State_in_LangGraph.ipynb` | State in LangGraph |
| `02_Nodes_in_LangGraph.ipynb` | Nodes in LangGraph |
| `03_Edges_in_LangGraph.ipynb` | Edges in LangGraph |
| `04_Creating_our_basic_Research_Agent.ipynb` | Creating our basic Research Agent (research agent v1) |
| `05_Understanding_Reducers_in_depth.ipynb` | Understanding Reducers in depth (Overwrite / List / Dict / Numeric) |
| `06_Creating_a_research_agent_with_parallel_nodes.ipynb` | Creating a research agent with parallel nodes (research agent v2) |
| `07_Caching_in_Nodes.ipynb` | Caching in Nodes (Cache Policy / Cache Store) |
| `08_Supervisor_Worker_model_in_LangGraph.ipynb` | Supervisor-Worker model in LangGraph (Supervisor Node, SEND/COMMAND, Worker Nodes, Subgraphs) |
| `09_Exercise_4_Creating_advanced_research_agent.ipynb` | Exercise 4: Creating advanced research agent (capstone) |

## Setup

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Copy `.env.example` to `.env` and fill in your keys:

```bash
copy .env.example .env
```

- `OPENAI_API_KEY` is used by notebooks 04, 06 and 09 to generate the final summary.
- `TAVILY_API_KEY` is used by notebooks 06 and 09 for the web-search branch.

**Every notebook runs without either key** -- the LLM/web-search nodes catch the missing-key
error, record it, and the graph completes anyway (matching the book's own `search_from_tavily`
pattern of catching and recording errors instead of crashing). Add the keys to see real search
results and a real generated summary instead of the "[Skipped ...]" placeholder text.

## Notes on fidelity to the book text

- Nodes return partial state updates (`return {"key": value}`) rather than mutating and
  returning the whole state object -- the pattern the book itself switches to once reducers are
  introduced, applied consistently from notebook 04 onward.
- A few helper functions the book references but doesn't define (`normalize_query`,
  `enrich_data`, `llm_summarize`, ...) are given simple one-line stand-ins in notebook 02/03.
- Notebook 09's `candidate_urls` reducer is `add_unique` (concatenate + dedupe) instead of the
  book's plain `operator.add` -- with a plain add, the `merge_results` dedup step in the search
  subgraph ends up re-adding the same URLs on top of themselves. `add_unique` is a two-line
  reducer that fixes that while keeping everything else from the chapter (see the Reducers
  notebook for how custom reducers like `keep_non_empty` work).
- All external calls (Wikipedia, Tavily, OpenAI, `requests.get`) are wrapped in `try/except` so
  a network hiccup or a missing key never crashes a whole notebook.
