from state import ResearchState
from langchain_community.retrievers import WikipediaRetriever
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

llm = ChatOpenAI(model_name="gpt-4", temperature=0.0)
wiki = WikipediaRetriever()

def prepare_query(state: ResearchState) -> ResearchState:
    query = state.get('query', '') if isinstance(state, dict) else state.query
    cleaned = query.strip().lower() if query else ""
    return {"query": cleaned}


def search_sources(state: ResearchState) -> ResearchState:    
    query = state.get('query', '') if isinstance(state, dict) else state.query
    
    print("\n" + "="*80)
    print("NODE: search_sources (REUSED from nodes.py)")
    print("="*80)
    print(f"\n[BEFORE] State:")
    print(f"  query: '{query}'")
    
    if not query or query.strip() == "":
        print(f"  - Skipping Wikipedia search (empty query)")
        print("="*80)
        return {"candidate_urls": [], "page_texts": []}
    
    print(f"\n[PROCESSING] Actions:")
    print(f"  - Searching Wikipedia for: '{query}'")
    
    urls = []
    texts = []
    
    try:
        docs = wiki.invoke(query)
        print(f"  - Found {len(docs)} Wikipedia documents")
        
        urls = []
        for doc in docs:
            url = doc.metadata.get("url", "")
            if not url or not url.startswith("http"):
                title = doc.metadata.get("title", "").replace(" ", "_")
                url = f"https://en.wikipedia.org/wiki/{title}"
            urls.append(url)
        
        texts = [doc.page_content for doc in docs]
        
        print(f"  - Extracted {len(urls)} URLs")
        if urls:
            print(f"    Sample URLs: {urls[:2]}")
        
    except Exception as e:
        print(f"  - Error searching Wikipedia: {str(e)}")
        urls = []
        texts = []
    
    print(f"\n[AFTER] State:")
    print(f"  candidate_urls: {len(urls)} Wikipedia URLs")
    print(f"  page_texts: {len(texts)} text snippets")
    print("="*80)
    
    return {"candidate_urls": urls, "page_texts": texts}


def summarize_results(state: ResearchState) -> ResearchState:    
    page_texts = state.get('page_texts', []) if isinstance(state, dict) else state.page_texts
    combined = "\n\n".join(page_texts)
    
    if not combined:
        return {"final_report": "No content found."}
    
    prompt = f"Summarize the key points and cite sources if needed:\n\n{combined}"
    summary = llm.invoke(prompt)
    
    return {"final_report": summary.content}

def decide_source(state: ResearchState) -> ResearchState:
    """Used to decide whether to use Wikipedia or Web Search as source."""
    pass
