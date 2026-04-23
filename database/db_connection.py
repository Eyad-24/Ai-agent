import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="ecommerce_ai",
        user="postgres",
        password="****",
        host="localhost",
        port="****"
    )

