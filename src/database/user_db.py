from src.database.connection import get_connection

def create_user(name, email):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO users (name, email) VALUES (%s, %s) RETURNING *;",
        (name, email)
    )

    user = cur.fetchone()
    conn.commit()

    cur.close()
    conn.close()

    return user


def get_user_by_id(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT * FROM users WHERE id = %s;", (user_id,))
    user = cur.fetchone()

    cur.close()
    conn.close()

    return user