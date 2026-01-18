from database.db_connection import get_connection

def log_search(user_id, query, result_count):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO search_logs (user_id, query, result_count)
        VALUES (%s, %s, %s)
        """,
        (user_id, query, result_count)
    )

    conn.commit()
    cur.close()
    conn.close()