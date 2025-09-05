import uuid
import typing
import datetime

from django.conf import settings
from django.utils import timezone
from django.contrib.auth import get_user_model

import jwt

from .models import Token

NOT_A_REFRESH_MESSAGE = "Not a refresh token"
UNKNOWN_REFRESH_MESSAGE = "Refresh token unknown"
REFRESH_INACTIVE_MESSAGE = "Refresh token inactive"

S = settings.JWT_SETTINGS

User = get_user_model()

class Payload(typing.TypedDict):
    """Typed dict of base jwt token claims."""

    iss: str
    sub: str
    aud: str
    iat: int
    exp: int
    nbf: int
    jti: str
    typ: Token.Kind


class TokensPair(typing.TypedDict):
    """Storages both access and refresh tokens."""

    access: str
    access_expiry: int
    refresh: str
    refresh_expiry: int
    user: User


def _base_claims(
    user: User,
    *,
    kind: Token.Kind,
    ttl: datetime.timedelta,
) -> Payload:
    """Return payload for jwt tokens encode."""
    now = timezone.now()
    return Payload(
        iss=S["ISSUSER"],
        sub=str(user.id),
        aud="api",
        iat=int(now.timestamp()),
        exp=int((now + ttl).timestamp()),
        nbf=int(now.timestamp()),
        jti=str(uuid.uuid4()),
        typ=kind.value,
    )


def issue_pair(
    user: User,
    *,
    user_agent: str = "",
    ip: str | None = None,
) -> TokensPair:
    """Return pair access plus refresh tokens and bulk create db instances."""
    access_claims = _base_claims(
        user=user,
        kind=Token.Kind.ACCESS,
        ttl=S["ACCESS_TTL"],
    )
    refresh_claims = _base_claims(
        user=user,
        kind=Token.Kind.REFRESH,
        ttl=S["REFRESH_TTL"],
    )

    access_token = jwt.encode(
        payload=access_claims,
        key=settings.SECRET_KEY,
        algorithm=S["HASH_ALGORITHM"],
    )
    refresh_token = jwt.encode(
        payload=refresh_claims,
        key=settings.SECRET_KEY,
        algorithm=S["HASH_ALGORITHM"],
    )

    Token.objects.bulk_create(
        [
            Token(
                user=user,
                kind=Token.Kind.ACCESS,
                jti=access_claims["jti"],
                issued=timezone.datetime.fromtimestamp(
                    access_claims["iat"],
                    tz=datetime.timezone.utc,
                ),
                expires=timezone.datetime.fromtimestamp(
                    access_claims["exp"],
                    tz=datetime.timezone.utc,
                ),
                user_agent=user_agent,
                ip=ip,
            ),
            Token(
                user=user,
                kind=Token.Kind.REFRESH,
                jti=refresh_claims["jti"],
                issued=timezone.datetime.fromtimestamp(
                    refresh_claims["iat"],
                    tz=datetime.timezone.utc,
                ),
                expires=timezone.datetime.fromtimestamp(
                    refresh_claims["exp"],
                    tz=datetime.timezone.utc,
                ),
                user_agent=user_agent,
                ip=ip,
            ),
        ],
    )

    return TokensPair(
        access=access_token,
        access_expiry=access_claims["exp"],
        refresh=refresh_token,
        refresh_expiry=refresh_claims["exp"],
        user=user,
    )


def decode_token(token: str) -> Payload:
    """Return and decode payload from jwt token."""
    return jwt.decode(
        jwt=token,
        key=settings.SECRET_KEY,
        algorithms=[
            S["HASH_ALGORITHM"],
        ],
        options={
            "verify_aud": False,
        },
        issuer=S["ISSUSER"],
    )


def revoke_by_jti(jti: str) -> None:
    """Return None and revoke token by jti."""
    Token.objects.filter(jti=jti, revoked=False).update(revoked=True)


def revoke_all_for_user(user: User) -> None:
    """Return None and revoke all tokens for user."""
    Token.objects.filter(user=user, revoked=False).update(revoked=True)


def rotate_refresh(
    old_refresh_token: str,
    *,
    user_agent: str = "",
    ip: str | None = None,
) -> TokensPair:
    """Return and invalidate old refresh by issue new pair."""
    claims = decode_token(token=old_refresh_token)
    if claims.get("typ") != "refresh":
        raise jwt.InvalidTokenError(NOT_A_REFRESH_MESSAGE)
    try:
        dbt = Token.objects.get(jti=claims["jti"], kind=Token.Kind.REFRESH)
    except Token.DoesNotExist:
        raise jwt.InvalidTokenError(UNKNOWN_REFRESH_MESSAGE)

    if not dbt.is_active():
        raise jwt.InvalidTokenError(REFRESH_INACTIVE_MESSAGE)

    dbt.revoked = True
    dbt.save(update_fields=["revoked"])
    user = dbt.user
    return issue_pair(user, user_agent=user_agent, ip=ip)
