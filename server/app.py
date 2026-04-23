from flask import Flask
from flask_cors import CORS
from server.config import Config
from server.extensions import db, bcrypt, jwt, migrate

# Import blueprints
from resources.auth import auth_bp
from resources.expenses import expense_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Enable CORS
    CORS(app)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(expense_bp)

    # Simple health check route
    @app.route("/")
    def home():
        return {"message": "Expense Tracker API is running"}, 200

    return app


# Create app instance
app = create_app()


if __name__ == "__main__":
    app.run(debug=True)