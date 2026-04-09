from backend.models.initialize import get_connection

def create_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS access_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            locker_id INTEGER NOT NULL,
            action TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (locker_id) REFERENCES lockers(id)
        )
    """)
    conn.commit()
    conn.close()

def log_access(user_id, locker_id, action):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO access_logs (user_id, locker_id, action) VALUES (?, ?, ?)",
            (user_id, locker_id, action)
        )
        conn.commit()
    except Exception as e:
        print(f"Failed to log access: {e}")
    finally:
        conn.close()

def get_all_access_logs():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.id, u.username, a.locker_id, a.action, a.timestamp
            FROM access_logs a
            JOIN users u ON a.user_id = u.id
            ORDER BY a.timestamp DESC
        """)
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    except Exception as e:
        print(f"Failed getting access logs: {e}")
        return []
    finally:
        conn.close()
