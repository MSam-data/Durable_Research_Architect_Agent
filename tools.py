import os
from duckduckgo_search import DDGS

def web_search(query: str) -> str:
    
    print(f"  [Action] Agent is searching the web for: '{query}'...")
    
    try:
        results_list = []
        with DDGS() as ddgs:
            # We fetch the top 4 results for a good balance of data and speed
            ddgs_gen = ddgs.text(query, max_results=4)
            for r in ddgs_gen:
                results_list.append(f"Source: {r['title']}\nContent: {r['body']}")
        
        if not results_list:
            return "No relevant web results found for this query."
            
        return "\n\n---\n\n".join(results_list)

    except Exception as e:
        return f"Error encountered during web search: {str(e)}"