# Chapter 10 -- Section Notebooks

One runnable Jupyter notebook per chapter section that has code, named after that section's
heading -- same convention as Chapters 4-9. No API keys or external services needed anywhere:
embeddings, vector/keyword search, and reranking all use small deterministic stand-ins (a
hashed-bag-of-words "embedding" and word-overlap scoring) instead of a real embedding model or
vector database, so every notebook runs fully offline.

| Notebook | Chapter section |
|---|---|
| `01_Document_Chunking_Strategies.ipynb` | fixed-size, sentence-aware, and parent-child chunking |
| `02_Embedding_and_Index_Design.ipynb` | a deterministic hashed embedding + a tiny in-memory vector store |
| `03_Hybrid_Search_and_Query_Routing.ipynb` | `hybrid_score`, `route_query` |
| `04_Metadata_Filters_and_Access_Control.ipynb` | `build_filters`, pre- and post-retrieval enforcement |
| `05_Reranking_and_Context_Selection.ipynb` | `select_context`, a score-gap rule |
| `06_Caching_and_Performance_Tuning.ipynb` | `timed_retrieve`, proven with a real call-counter |
| `07_MCP_Integration_for_Retrieval_Services.ipynb` | a real MCP server exposing `search_docs` (tool) + `resource://kb/{doc_id}` (resource) |
| `08_LangGraph_Pattern_for_RAG_Workflows.ipynb` | `RAGState`, `route_after_assess`, a full rewrite/retrieve/rerank/assess/generate graph with a capped retry loop |
| `09_Example_Production_RAG_with_Python.ipynb` | the book's capstone: `chunk_doc`, `ingest`, `search`, and an MCP-backed `retrieve_node`, tied together |
| `10_RAG_Evaluation_and_Debugging.ipynb` | hit rate, context relevance, answer relevance, faithfulness, a before/after debugging loop |
| `11_Common_Pitfalls.ipynb` | staleness checks, `safe_context` (prompt-injection stripping), metadata validation, fallback design |

**Every notebook is self-contained and order-independent** -- run any one on its own, in any
order. Notebooks 07 and 09 each write their own distinctly-named MCP server
(`retrieval_server.py`, `production_rag_server.py`) via `%%writefile`, so they don't depend on
each other either.

## Setup

```bash
pip install -r requirements.txt
```

## Notes on fidelity to the book text

- The book's chunking, hybrid-search, filtering, reranking, caching, MCP, and RAG-state code
  blocks are reproduced unchanged; helper objects they call into (an embedder, a reranker, an MCP
  client) are small, clearly-labeled, deterministic stand-ins so every function actually runs.
- `retrieve_node` (notebooks 08 and 09) is shown in the book as a plain `def`, but a real MCP tool
  call is awaitable -- it's `async def` here so it can actually reach the server, noted at the
  point it's defined.
- The "fake embedding" is a hashed bag-of-words (the same hashing trick real systems like
  scikit-learn's `HashingVectorizer` use), with a one-line naive stemmer (`words` -> `word`) so
  "refund" and "refunds" land in the same bucket -- without it, the retrieval demos returned empty
  results, since a real semantic match ("refund" ~ "refunds") looks like a total mismatch to exact
  string hashing.
- Two gaps were filled with small, clearly-labeled implementations because the book names the
  behavior but doesn't give code for it: a parent-child chunker (built on sentence boundaries for
  *both* levels, not a raw fixed-size cut, which would otherwise slice a parent chunk mid-word) and
  the `context_relevance` / `answer_relevance` / `faithfulness` scoring functions in notebook 10
  (word-overlap proxies, not a real NLI/grading model).
