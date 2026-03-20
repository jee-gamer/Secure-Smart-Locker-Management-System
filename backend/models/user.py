from backend.models.initialize import get_connection
from werkzeug.security import generate_password_hash

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()

def db_create_user(username, password, role='user'):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)
    try:
        cursor.execute(
            "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
            (username, hashed_password, role)
        )
        conn.commit()
    except conn.IntegrityError:
        # This will happen if the username is already taken (due to UNIQUE constraint)
        # We can ignore it for a seeding script.
        pass
    finally:
        conn.close()

def db_get_user_by_username(username):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE username = ?", (username,)
    )

    user = cursor.fetchone() # will return None if none is found
    conn.close()
    return dict(user) if user else None

def db_get_all_users():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, username, role FROM users")
    rows = cursor.fetchall()

    conn.close()
    return [dict(r) for r in rows]

def seed_initial_users():
    """Creates a set of predefined users if they don't exist."""
    users_to_create = [
        {"username": "man", "password": "1234"},
        {"username": "user1", "password": "1234"},
        {"username": "user2", "password": "1234"},
        {"username": "stupid", "password": "1234"},
    ]
    print("Seeding initial users...")
    for user_data in users_to_create:
        db_create_user(user_data["username"], user_data["password"])
    print("User seeding complete.")
