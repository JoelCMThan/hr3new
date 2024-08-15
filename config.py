import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Session management settings
    PERMANENT_SESSION_LIFETIME = timedelta(minutes=30)  # Set session to expire after 30 minutes of inactivity
    SESSION_COOKIE_SECURE = True  # Ensures cookies are only sent over HTTPS
    SESSION_COOKIE_HTTPONLY = True  # Prevents JavaScript access to session cookies
    SESSION_COOKIE_SAMESITE = 'Lax'  # Helps prevent CSRF attacks

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///site.db'
