import os
import requests

# 1
def search_products(query: str):
    api_key = os.getenv("SERPAPI_API_KEY")
    if not api_key:
        raise ValueError("SERPAPI_API_KEY not set in environment variables.")

    params = {
        "engine": "google_shopping",
        "q": query,
        "SERPAPI_API_KEY": api_key
    }

    response = requests.get("https://serpapi.com/search", params=params)
    results = response.json()

    if "error" in results:
        raise ValueError(f"SerpAPI Error: {results['error']}")

    products = []
    for item in results.get("shopping_results", [])[:5]: #Limit to 5 results
        products.append({
            "name": item.get("title", "Unknown"),
            "price": item.get("price", "N/A"),
            "rating": item.get("rating", "N/A"),
            "link": item.get("link", "#") 
        })

    return products
