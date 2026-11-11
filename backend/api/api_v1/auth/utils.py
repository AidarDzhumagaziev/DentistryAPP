import uuid

import bcrypt
import jwt

from datetime import datetime, timedelta, timezone

from api.api_v1.users.schemas import UserRead
from core.config import settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"


def encode_jwt(
    payload: dict,
    private_key: str = settings.auth_jwt.private_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(timezone.utc)
    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)
    to_encode.update(exp=expire, iat=now, jti=str(uuid.uuid4()))
    encoded = jwt.encode(payload=to_encode, key=private_key, algorithm=algorithm)
    return encoded


def decode_jwt(
    token: str | bytes,
    public_key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    decoded = jwt.decode(jwt=token, key=public_key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def validate_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


def create_jwt(
    token_type: str,
    token_data: dict,
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
    expire_timedelta: timedelta | None = None,
):
    jwt_payload = {TOKEN_TYPE_FIELD: token_type}
    jwt_payload.update(token_data)
    return encode_jwt(
        jwt_payload, expire_minutes=expire_minutes, expire_timedelta=expire_timedelta
    )


def create_access_token(user: UserRead):
    payload = {
        "sub": str(user.id),
        "role": str(user.role),
    }
    return create_jwt(token_type=ACCESS_TOKEN_TYPE, token_data=payload)


def create_refresh_token(user: UserRead):
    payload = {"sub": str(user.id)}
    return create_jwt(
        token_type=REFRESH_TOKEN_TYPE,
        token_data=payload,
        expire_timedelta=timedelta(settings.auth_jwt.refresh_token_expire_days),
    )
