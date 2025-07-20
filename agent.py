import os
from dotenv import load_dotenv
from serpapi import GoogleSearch
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage

load_dotenv()  # Loads SERPAPI_API_KEY from .env

# 1- Product search helper
def search_products(user_query: str) -> list[dict]:
    """Return up to 5 product dicts with title, price, rating, link."""

    api_key = os.getenv("SERPAPI_API_KEY")
    
    if not api_key:
        raise ValueError(
            "❌ SERPAPI_API_KEY not set. "
            "Add it to .env or your system environment."
        )

    params = {
        "engine": "google_shopping",
        "q": user_query,
        "hl": "en",
        "gl": "us",
        "api_key": api_key,
    }

    results = GoogleSearch(params).get_dict()

    if "error" in results:
        raise ValueError(f"SerpAPI Error: {results['error']}")

    products_raw = results.get("shopping_results", [])
    top_matches: list[dict] = []

    for item in products_raw[:5]:
        title  = item.get("title",  "No title")
        price  = item.get("price",  "N/A")
        rating = item.get("rating", "N/A")

        # Try several possible link keys
        link = (
            item.get("link")
            or item.get("product_link")
            or item.get("source")
            or "#"
        )

        # Keep only valid absolute URLs
        if not link.startswith(("http://", "https://")):
            continue

        top_matches.append(
            {"title": title, "price": price, "rating": rating, "link": link}
        )
        
    return top_matches

# 2- AI suggestion helper
def generate_ai_suggestion(user_query: str) -> str:
    """Short 1‑product suggestion written by GPT."""
    llm = ChatOpenAI(model="gpt-3.5-turbo", temperature=0.7)
    prompt = (
        "Suggest exactly ONE specific product that satisfies this request:\n"
        f"\"{user_query}\"\n"
        "Explain briefly (one sentence) why it's a good choice."
    )

    response = llm([HumanMessage(content=prompt)])
    return response.content.strip()
