# Chapter 5 -- Section Notebooks

One runnable Jupyter notebook per chapter section that contains code, named after that
section's heading -- same convention as Chapter 4's `section-notebooks/`.

| Notebook | Chapter section |
|---|---|
| `01_Building_Research_agent_with_tools_without_MCP.ipynb` | Building Research agent with tools without MCP |
| `02_Tools_in_MCP.ipynb` | Tools in MCP (tool descriptors, JSON-RPC message format) |
| `03_Building_an_MCP_Server_in_Python.ipynb` | Building an MCP Server in Python |
| `04_Building_an_MCP_client.ipynb` | Building an MCP client (STDIO and SSE transports) |
| `05_Connecting_LangGraph_with_MCP.ipynb` | Connecting LangGraph with MCP |

**Run order matters here, unlike Chapter 4's notebooks.** Notebooks 04 and 05 both launch
`server.py` as a subprocess, and that file only exists once notebook 03 has been run (it writes
`server.py` to this same folder via the `%%writefile` magic). Run **03 before 04 and 05**; 01 and
02 can run any time.

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

- `OPENAI_API_KEY` is used by notebooks 01 and 05 to run the LLM that decides which tool to call.
- `TAVILY_API_KEY` is used by the `search_web` tool in notebooks 01, 03 (the server), and 04.

**Every notebook runs without either key** -- missing-key paths print a clear message and the
notebook still completes, the same pattern used throughout Chapter 4's notebooks.

## Notes on fidelity to the book text

- The book constructs `TavilySearchResults(...)` once at server module-import time. That
  validates `TAVILY_API_KEY` immediately, so with no key set the whole MCP server process would
  crash on startup -- taking `search_wikipedia` down with it too. Notebook 03's `server.py`
  builds `TavilySearchResults` lazily, inside `search_web()` itself, so a missing key only
  affects that one tool call.
- Notebooks 04 and 05 add a small, Windows-only fix at the top (guarded by `os.name == "nt"`):
  Jupyter's `sys.stderr` has no real OS file descriptor, and the MCP SDK's Windows
  subprocess-launch fallback needs one, so on Windows the notebook swaps in a real one before
  spawning `server.py`. This isn't needed (or applied) on Linux/Mac.
- Notebooks 04 and 05 use top-level `await` instead of the book's `asyncio.run(main())`, because
  Jupyter already runs its own asyncio event loop and `asyncio.run()` cannot be nested inside one.
- The SSE cell in notebook 04 expects a second server running separately (`python server.py sse`
  in another terminal). Without one, it prints a connection-failure message instead of crashing --
  exactly how the book's own client code handles it.
