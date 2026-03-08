from backend.models.initialize import get_connection
from datetime import datetime

def create_table():
    """
    status: True = Occupied, False = Available
    :return:
    """
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS bookings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            locker_id INTEGER NOT NULL,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (locker_id) REFERENCES lockers(id)
        )
    """)

    conn.commit()
    conn.close()

def book(user_id, receiver_id, locker_id, item):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO bookings (user_id, receiver_id, locker_id) VALUES (?, ?, ?)",
            (user_id, receiver_id, locker_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Booking failed: {e}")
        return False
    finally:
        conn.close()

def unbook(user_id, locker_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "UPDATE bookings SET end_time = ? WHERE user_id = ? AND locker_id = ?",
            (datetime.now(), user_id, locker_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Booking failed: {e}")
        return False
    finally:
        conn.close()

def is_active(user_id, locker_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM bookings WHERE user_id = ? AND locker_id = ? AND end_time IS NULL",
        (user_id, locker_id)
    )

    if cursor.fetchone():
        return True

    return False