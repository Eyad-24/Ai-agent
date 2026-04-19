from database.db_connection import get_connection

def log_search(user_id, query, result_count, source):
    conn = get_connection()
    cur = conn.cursor()

    sql = """
        INSERT INTO search_logs (user_id, query, result_count, source)
        VALUES (%s, %s, %s, %s)
    """
    cur.execute(sql, (user_id, query, result_count, source))
    conn.commit()
    
    cur.close()
    conn.close()