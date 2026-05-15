from __future__ import annotations

import os
from datetime import timedelta
from typing import TYPE_CHECKING

from dotenv import load_dotenv

if TYPE_CHECKING:
    from flask import Flask

load_dotenv()


def get_secret_key() -> str:
    key = os.environ.get('FLASK_SECRET_KEY', '').strip()
    if not key:
        raise RuntimeError(
            'FLASK_SECRET_KEY is not set. Copy .env.example to .env '
            'and set a long random secret key.'
        )
    return key


def configure_app(app: Flask) -> None:
    """Apply shared Flask security settings (CSRF, cookies, secret key)."""
    app.config['SECRET_KEY'] = get_secret_key()
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['WTF_CSRF_TIME_LIMIT'] = int(
        os.environ.get('WTF_CSRF_TIME_LIMIT', '3600'))
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.config['SESSION_COOKIE_SECURE'] = (
        os.environ.get('FLASK_ENV', 'development').lower() == 'production'
    )
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(
        days=int(os.environ.get('SESSION_LIFETIME_DAYS', '14')))
