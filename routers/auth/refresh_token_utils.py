import secrets
import uuid
from datetime import datetime, timezone, timedelta
import hashlib
import jwt
from os import getenv
import hmac

from fastapi import HTTPException
from starlette import status

from database.db_models.RefreshToken import RefreshToken
from database.db_models.users import Users
from database.db_utils.db_dependency import db_dependency
from routers.auth.auth_utils import ALGORITHM

REFRESH_SECRET_KEY = getenv("REFRESH_SECRET_KEY")
# Tolerates concurrent refreshes that race on the same token after rotation
REUSE_GRACE_PERIOD = timedelta(seconds=10)


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def create_refresh_token(user_id: int, expires_delta: timedelta, db: db_dependency, family_id: str | None = None) -> str:
    jti = uuid.uuid4().hex
    expires_at = datetime.now(timezone.utc) + expires_delta

    payload = {
        "sub": str(user_id),  # PyJWT >= 2.10 rejects non-string "sub"
        "jti": jti,
        "token_type": "refresh",
        "exp": expires_at,
    }
    token = jwt.encode(payload, REFRESH_SECRET_KEY, algorithm=ALGORITHM)

    db.add(RefreshToken(
        jti=jti,
        family_id=family_id or uuid.uuid4().hex,
        user_id=user_id,
        token_hash=_hash_token(token),
        expires_at=expires_at,
    ))
    db.commit()
    return token

def _unauthorized(detail: str = "Invalid refresh token"):
    return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


def validate_refresh_token(token: str, db) -> tuple[RefreshToken, Users]:
    # 1. Signature + expiry
    try:
        payload = jwt.decode(token, REFRESH_SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.InvalidTokenError:  # PyJWT exception, also covers ExpiredSignatureError
        raise _unauthorized()

    # 2. Claims
    jti = payload.get("jti")
    user_id = payload.get("sub")
    token_type = payload.get("token_type")
    if token_type != "refresh" or not jti or not user_id:
        raise _unauthorized()

    # 3. DB record
    record = db.query(RefreshToken).filter(RefreshToken.jti == jti).first()
    if record is None or record.user_id != int(user_id):
        raise _unauthorized()

    # 4. Hash match (constant-time)
    if not hmac.compare_digest(record.token_hash, _hash_token(token)):
        raise _unauthorized()

    # 5. Revoked -> allow within grace period, otherwise treat as theft and kill the whole family
    if record.revoked_at is not None:
        if datetime.now(timezone.utc) - record.revoked_at > REUSE_GRACE_PERIOD:
            revoke_family(db, record.family_id)
            raise _unauthorized("Refresh token reuse detected")

    # 6. User still valid
    user = db.query(Users).filter(Users.id == record.user_id).first()
    if user is None or not user.is_active:
        raise _unauthorized()

    return record, user

def revoke_token(db, record: RefreshToken):
    # Keep the original timestamp so repeated use can't extend the grace window
    if record.revoked_at is None:
        record.revoked_at = datetime.now(timezone.utc)
        db.commit()


def revoke_family(db, family_id: str):
    db.query(RefreshToken).filter(
        RefreshToken.family_id == family_id,
        RefreshToken.revoked_at.is_(None), # SQLAlchemy filter for non-revoked tokens( Column Object IS NULL)
    ).update({RefreshToken.revoked_at: datetime.now(timezone.utc)})
    db.commit()