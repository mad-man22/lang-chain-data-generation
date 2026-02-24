from duckduckgo_search import DDGS
from src.schema import ParameterSpec
import time

search_tool = DDGS()

def search_ddgs(query):
    try:
        results = search_tool.text(query, max_results=5)
        return "\\n".join([r.get("body", "") for r in results])
    except Exception as e:
        print(f"Search tool error for {query}: {e}")
        return ""

def generation_prompt(company_name: str, specs: list[ParameterSpec]) -> str:
    print(f"[{company_name}] Searching for context...")
    
    search_1 = search_ddgs(f"{company_name} company overview headquarters revenue employees")
    time.sleep(1)
    search_2 = search_ddgs(f"{company_name} technology stack competitors market")
    time.sleep(1)
    search_3 = search_ddgs(f"{company_name} recent news funding investors")
    
    context = f"Search Results 1:\n{search_1}\n\nSearch Results 2:\n{search_2}\n\nSearch Results 3:\n{search_3}"

    # Load the base prompt rules
    with open("data/input/prompt_text.txt", "r", encoding="utf-8") as f:
        base_prompt_text = f.read()
        
    # Replace the placeholder "Blinkit" with the targeted company
    prompt_str = base_prompt_text.replace("Blinkit", company_name)
    
    final_prompt = f"Context from Recent Web Searches:\n{context}\n\n{prompt_str}"
    
    # We add a specific instruction to ensure the AI knows to output the table
    final_prompt += "\n\nYou are an expert Corporate Intelligence Analyst. Use the provided web search context to augment your internal database. Follow all instructions strictly, especially regarding the Markdown table format. Ensure every ID from 1 to 163 is present in the table."
    
    return final_prompt
