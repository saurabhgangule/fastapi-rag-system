import logging
import os
from datetime import datetime, timedelta

import bcrypt
import jwt
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")


def create_access_token(user_id: int, expires_minutes: int = 60):
    """Create a JWT access token"""

    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=expires_minutes),
    }
    encoded_jwt = jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    return encoded_jwt


def verify_token(token: str):
    """Verify a JWT access token"""

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload

    except jwt.ExpiredSignatureError:
        raise Exception("Token has expired")
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


def hash_password(password: str):
    """Hash a password"""

    try:
        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        return hashed.decode("utf-8")

    except Exception as e:
        logger.error(f"Failed to hash password: {e}")
        raise Exception("Failed to hash password")


def check_password(password: str, hashed_password: str):
    """Check a password"""

    try:
        password_bytes = password.encode("utf-8")
        hashed_bytes = hashed_password.encode("utf-8")

        return bcrypt.checkpw(password_bytes, hashed_bytes)

    except Exception as e:
        logger.error(f"Password check failed: {e}")
        raise Exception("Password verification failed")
