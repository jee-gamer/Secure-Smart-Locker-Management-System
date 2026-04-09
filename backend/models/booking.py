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

def book(user_id, receiver_id, locker_id):
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
            "UPDATE bookings SET end_time = CURRENT_TIMESTAMP WHERE user_id = ? AND locker_id = ?",
            (user_id, locker_id)
        )
        conn.commit()
        return True
    except Exception as e:
        print(f"Booking failed: {e}")
        return False
    finally:
        conn.close()

def is_active(user_id, locker_id) -> bool:
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM bookings WHERE user_id = ? AND locker_id = ? AND end_time IS NULL",
            (user_id, locker_id)
        )

        if cursor.fetchone():
            return True
    except Exception as e:
        print(f"Checking for active booking failed: {e}")
        return False
    finally:
        conn.close()

    return False

def get_all_active_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "SELECT * FROM bookings WHERE end_time IS NULL"
        )
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Getting active bookings failed: {e}")
        return None
    finally:
        conn.close()

def get_all_bookings():
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT b.id, b.start_time, b.end_time, b.locker_id,
                   s.username AS sender, r.username AS receiver
            FROM bookings b
            JOIN users s ON b.user_id = s.id
            JOIN users r ON b.receiver_id = r.id
            ORDER BY b.start_time DESC
        ''')
        rows = cursor.fetchall()
        return [dict(r) for r in rows]
    except Exception as e:
        print(f"Getting all bookings failed: {e}")
        return None
    finally:
        conn.close()

def get_booking_for_locker(locker_id):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        # THERE SHOULD ONLY BE ONE
        cursor.execute(
            "SELECT * FROM bookings WHERE locker_id = ? AND end_time IS NULL",
            (locker_id,)
        )
        row = cursor.fetchone()
        return dict(row) if row else None
    except Exception as e:
        print(f"Getting booking for locker: {locker_id} failed: {e}")
        return None
    finally:
        conn.close()
