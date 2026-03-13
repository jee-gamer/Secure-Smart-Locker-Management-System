from backend.models.initialize import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lockers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            status TEXT NOT NULL CHECK(status IN ('available', 'occupied'))
        )
    """)

    conn.commit()
    conn.close()

def seed_lockers():
    """Seed 25 lockers if they don't exist yet."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM lockers")
    count = cursor.fetchone()[0]
    if count == 0:
        cursor.executemany(
            "INSERT INTO lockers (status) VALUES (?)",
            [('available',)] * 25
        )
        conn.commit()

    conn.close()

def db_get_all_lockers():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id, status, location FROM lockers ORDER BY id")
    rows = cursor.fetchall()

    conn.close()

    return [dict(r) for r in rows]

def db_get_locker_with_booking(locker_id):
    """Return locker info + active booking details by integer locker id."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            l.id, l.status, l.location,
            b.id AS booking_id,
            b.user_id AS sender_id,
            sender.username AS sender_username,
            b.receiver_id,
            receiver.username AS receiver_username
        FROM lockers l
        LEFT JOIN bookings b ON b.locker_id = l.id AND b.end_time IS NULL
        LEFT JOIN users sender ON sender.id = b.user_id
        LEFT JOIN users receiver ON receiver.id = b.receiver_id
        WHERE l.id = ?
    """, (locker_id,))

    row = cursor.fetchone()

    conn.close()

    return dict(row) if row else None

def is_occupied(locker_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT status FROM lockers WHERE id = ?",
        (locker_id,)
    )

    locker_status = cursor.fetchone()
    if locker_status is None:
        return False
    if locker_status[0] == "occupied":
        return True

    return False

def set_status(locker_id, status):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE lockers SET status = ? WHERE id = ?",
            (status, locker_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Update locker status failed: {e}")
        return False
    finally:
        conn.close()
