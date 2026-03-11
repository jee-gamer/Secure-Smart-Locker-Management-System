from flask import Flask
from backend.models.migrate import run_migrations
from backend.routes.user_routes import user_bp
from backend.routes.booking_routes import booking_bp

def create_app():
    app = Flask(__name__)

    # Initialize the database tables
    run_migrations()

    # Register blueprints (routes)
    app.register_blueprint(user_bp)
    app.register_blueprint(booking_bp)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
