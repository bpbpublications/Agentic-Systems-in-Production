import os
import sys
from mcp.server.fastmcp import FastMCP
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("SearchServer")

wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())


@mcp.tool()
def search_wikipedia(query: str) -> str:
    """Search Wikipedia for information about people, places, facts, and history."""
    return wikipedia_tool.invoke(query)


@mcp.tool()
def search_web(query: str) -> str:
    """Search the web for current events, news, or general queries using Tavily."""
    # Built lazily: TavilySearchResults validates TAVILY_API_KEY at construction, which
    # would otherwise crash the whole server process on startup when the key is unset.
    if not os.environ.get("TAVILY_API_KEY"):
        return "TAVILY_API_KEY not set - cannot search the web."
    tavily_tool = TavilySearchResults(max_results=3, search_depth="advanced")
    result = tavily_tool.invoke({"query": query})
    return str(result)


if __name__ == "__main__":
    protocol = sys.argv[1] if len(sys.argv) > 1 else "stdio"
    if protocol == "sse":
        print("Starting MCP Server with SSE transport on http://localhost:8000/sse")
        mcp.run(transport="sse")
    else:
        mcp.run(transport="stdio")
