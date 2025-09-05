from django.contrib.auth import get_user_model
from rest_framework.request import Request
from rest_framework.authentication import (
    BaseAuthentication,
    get_authorization_header,
)
from rest_framework.exceptions import (
    AuthenticationFailed,
)

from .models import Token
from .utils import decode_token

VALID_AUTH_HEADER_LEN = 2
INVALID_AUTH_HEADER_MESSAGE = "Invalid authorization header"
INVALID_TOKEN_MESSAGE = "Invalid token: {error}"
TOKEN_REQUIRED_MESSAGE = "Access token required"
TOKEN_NOT_RECOGNIZED = "Token not recognized"
INACTIVE_TOKEN_MESSAGE = "Token inactive"
USER_NOT_FOUND_MESSAGE = "User not found or inactive"

User = get_user_model()

class JWTAuthentication(BaseAuthentication):
    """Authentication scheme for custom jwt tokens."""

    keyword = b"Bearer"

    def authenticate(self, request: Request) -> tuple[User, str]:
        """
        User jwt authentication.
        Return tuple of user instance and token.
        Raises `AuthenticationFailed` if credentials are invalid.
        """
        auth = get_authorization_header(request).split()
        if not auth or auth[0].lower() != self.keyword.lower():
            return None
        self.validate_auth_header(auth)
        token = self.get_token_from_header(auth)
        try:
            claims = decode_token(token)
        except Exception as error:
            raise AuthenticationFailed(
                INVALID_TOKEN_MESSAGE.format(
                    error=error,
                ),
            )

        if claims.get("typ") != Token.Kind.ACCESS.value:
            raise AuthenticationFailed(TOKEN_REQUIRED_MESSAGE)

        try:
            dbt = Token.objects.get(jti=claims["jti"], kind=Token.Kind.ACCESS)
        except Token.DoesNotExist:
            raise AuthenticationFailed(TOKEN_NOT_RECOGNIZED)
        if not dbt.is_active():
            raise AuthenticationFailed(INACTIVE_TOKEN_MESSAGE)

        try:
            user = User.objects.get(id=int(claims["sub"]), is_active=True)
        except User.DoesNotExist:
            raise AuthenticationFailed(USER_NOT_FOUND_MESSAGE)
        return user, token

    def validate_auth_header(self, header: bytearray) -> None:
        """Return None and Validate header or raise exception if it invalid."""
        if len(header) != VALID_AUTH_HEADER_LEN:
            raise AuthenticationFailed(INVALID_AUTH_HEADER_MESSAGE)

    def get_token_from_header(self, header: bytearray) -> str:
        """Return decoded token from header."""
        return header[1].decode("utf-8")
