import csv
from db_connection import get_connection

def seed_products():
    conn = get_connection()
    cur = conn.cursor()

    with open("data/products.csv", newline='', encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            cur.execute(
                """
                INSERT INTO products (name, category, price, description, rating, rating_count)
                VALUES (%s, %s, %s, %s, %s, %s)
                """,
                (
                    row.get("title"),
                    row.get("breadcrumbs"),
                    float(row.get("price_value")) if row.get("price_value") else None,
                    row.get("product_description") or row.get("about_item"),
                    float(row.get("rating_stars")) if row.get("rating_stars") else None,
                    int(row.get("rating_count")) if row.get("rating_count") else None
                )
            )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Products inserted successfully")

if __name__ == "__main__":
    seed_products()
