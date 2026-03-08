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

def is_occupied(locker_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM lockers WHERE locker_number = ?",
        (locker_id,)
    )

    locker_status = cursor.fetchone()
    if locker_status[0] == "occupied":
        return True

    return False

def set_status(locker_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE lockers SET status = ? WHERE locker_number = ?",
            (status, locker_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Update locker status failed: {e}")
        return False
    finally:
        conn.close()
