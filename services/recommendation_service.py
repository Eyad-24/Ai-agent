from database.db_connection import get_connection

def recommend_similar_products(product_title: str, limit: int = 3):
    """
    Recommend similar products based on product title similarity.
    This is a simple content-based recommendation approach.
    """

    keywords = product_title.lower().split()
    conn = get_connection()
    cur = conn.cursor()

    # Build dynamic SQL query using keywords
    conditions = " OR ".join(["LOWER(name) LIKE %s" for _ in keywords])
    values = [f"%{kw}%" for kw in keywords]

    query = f"""
        SELECT name, price, rating
        FROM products
        WHERE ({conditions})
          AND LOWER(name) != %s
        LIMIT %s;
    """

    cur.execute(query, values + [product_title.lower(), limit])
    rows = cur.fetchall()

    cur.close()
    conn.close()

    recommendations = []
    for row in rows:
        recommendations.append({
            "title": row[0],
            "price": row[1],
            "rating": row[2]
        })

    return recommendations