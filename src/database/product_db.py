from src.database.connection import get_connection

def get_all_products():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM products;")
    products = cur.fetchall()

    cur.close()
    conn.close()

    return products