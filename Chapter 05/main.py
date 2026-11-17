from graph import builder
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# Compile the graph into a runnable
graph = builder.compile()
initial_state = {
    "query": "Latest research on quantum computing",
    "candidate_urls": [],
    "page_texts": [],
    "draft_summary": "",
    "final_report": "",
    "errors": []
}

final_state = graph.invoke(initial_state)

print("\n" + "="*80)
print("FINAL REPORT")
print("="*80)
print(f"\nQuery: {final_state['query']}")

print(f"\nSources ({len(final_state['candidate_urls'])} found):")
if final_state['candidate_urls']:
    for i, url in enumerate(final_state['candidate_urls'], 1):
        print(f"  {i}. {url}")
else:
    print("  (No sources found)")

print(f"\nSummary:")
print(f"{final_state['final_report']}")

print(f"\nCited Sources:")
if final_state['candidate_urls']:
    for url in final_state['candidate_urls']:
        if not url or url.strip() == "":
            continue
        # Extract page title from URL for display
        if url.startswith('http'):
            # Parse title from URL
            if 'wikipedia.org' in url:
                title = url.split('/wiki/')[-1].replace('_', ' ')
            else:
                # For other URLs, try to extract a meaningful title
                title = url.split('/')[-1].strip() or 'Source'
        else:
            title = url
        
        # Skip empty titles
        if title and title.strip():
            print(f"  - [{title}]({url})")
else:
    print("  (No sources cited)")

if final_state['errors']:
    print(f"\nErrors encountered:")
    for error in final_state['errors']:
        print(f"  - {error}")

print("\n" + "="*80)