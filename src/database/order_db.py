from src.database.connection import get_connection

def create_order(user_id, total):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO orders (user_id, total) VALUES (%s, %s) RETURNING *;",
        (user_id, total)
    )

    order = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return order