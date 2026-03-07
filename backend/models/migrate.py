from backend.models import user, locker, booking

def run_migrations():
    user.create_table()
    locker.create_table()
    booking.create_table()
    print("Database initialized.")

if __name__ == "__main__":
    run_migrations()