"""
Centralized configuration.

Everything environment-specific (secret key, database path, debug mode, log
level) lives here and is read from environment variables where possible.
Locally this falls back to sane defaults so `python web_app.py` still just
works without any setup. On a real host (Render, Railway, Fly.io, etc.) you
set these as actual environment variables instead of editing code.
"""

import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "data/business.db")
    DEBUG = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = os.environ.get("LOG_FILE", "logs/app.log")

    @staticmethod
    def is_production():
        return os.environ.get("FLASK_ENV", "development") == "production"
