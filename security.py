"""비밀번호 해시 + JWT 발급/검증"""
import os
from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

# 실제 서비스에서는 반드시 환경변수 SECRET_KEY 로 바꿔서 사용 (예: openssl rand -hex 32)
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def _to_bytes(password: str) -> bytes:
    # bcrypt 는 72바이트까지만 사용하므로 같은 규칙으로 자름
    return password.encode("utf-8")[:72]


def hash_password(password: str) -> str:
    return bcrypt.hashpw(_to_bytes(password), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(_to_bytes(password), hashed_password.encode("utf-8"))


def create_access_token(user_id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    payload = {"sub": user_id, "exp": expire}  # sub = 토큰 주인(user_id)
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
