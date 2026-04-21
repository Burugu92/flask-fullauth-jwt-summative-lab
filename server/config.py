import os


class Config:
    # Base directory of the project
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))

    # Database configuration (SQLite)
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASE_DIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # JWT configuration
    JWT_SECRET_KEY = "super-secret-key"  # Change this to a strong secret key in production

    # Optional: Token expiration (1 hour)
    JWT_ACCESS_TOKEN_EXPIRES = 3600