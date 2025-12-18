import psycopg2

def get_connection():
    return psycopg2.connect(
        dbname="ecommerce_ai",
        user="postgres",
        password="1111",
        host="localhost",
        port="5432"
    )

