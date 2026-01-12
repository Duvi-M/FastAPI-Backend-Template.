from datetime import datetime, timedelta, timezone
from jose import jwt
from passlib.context import CryptContext
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    return pwd_context.verify(password, hashed)

def create_token(sub: str, token_type: str, expires_delta: timedelta) -> str:
    now = datetime.now(timezone.utc)
    payload = {"sub": sub, "type": token_type, "iat": int(now.timestamp()), "exp": now + expires_delta}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALG)

def create_access_token(sub: str) -> str:
    return create_token(sub, "access", timedelta(minutes=settings.ACCESS_TOKEN_MINUTES))

def create_refresh_token(sub: str) -> str:
    return create_token(sub, "refresh", timedelta(days=settings.REFRESH_TOKEN_DAYS))