import os
import requests
from database.db_connection import get_connection


# Database Product Search (Primary Source)
def search_products_db(query: str, limit: int = 5):
    """
    Search for products inside the local PostgreSQL database.
    This function is used as the PRIMARY search source before calling SerpAPI.
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT name, price, rating
        FROM products
        WHERE LOWER(name) LIKE %s
           OR LOWER(description) LIKE %s
        LIMIT %s;
        """,
        (f"%{query.lower()}%", f"%{query.lower()}%", limit)
    )

    rows = cur.fetchall()
    cur.close()
    conn.close()

    products = []
    for row in rows:
        products.append({
            "title": row[0],
            "price": row[1],
            "rating": row[2],
            "link": None, 
            "source": "database"  # Used to identify DB results
        })

    return products


# SerpAPI Product Search (Fallback Source)

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
