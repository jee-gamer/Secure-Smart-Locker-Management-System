from backend.models.initialize import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lockers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            locker_number TEXT NOT NULL UNIQUE,
            status TEXT NOT NULL CHECK(status IN ('available', 'occupied')),
            location TEXT
        )
    """)

    conn.commit()
    conn.close()

