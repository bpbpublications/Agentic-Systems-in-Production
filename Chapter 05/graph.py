from langgraph.graph import StateGraph, START, END
from state import ResearchState
from nodes import prepare_query, search_sources, summarize_results

builder = StateGraph(ResearchState)

builder.add_node("prepare_query", prepare_query)
builder.add_node("search_sources", search_sources)
builder.add_node("summarize_results", summarize_results)

# Connect the nodes: START -> prepare_query -> search_sources -> summarize_results -> END
builder.add_edge(START, "prepare_query")
builder.add_edge("prepare_query", "search_sources")
builder.add_edge("search_sources", "summarize_results")
builder.add_edge("summarize_results", END)
