from django.contrib.auth import login, get_user_model

from rest_framework import permissions, status
from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework.request import Request

import jwt

from ...authentication import JWTAuthentication
from . import serializers
from ...utils import (
    decode_token,
    revoke_by_jti,
    issue_pair,
    rotate_refresh,
    revoke_all_for_user,
)

User = get_user_model()

class RegisterView(CreateAPIView):
    """Register for new users view."""

    serializer_class = serializers.RegisterSerializer
    permission_classes = [permissions.AllowAny]
    authentication_classes = [JWTAuthentication]

    def create(self, request: Request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "detail": "User registered successfully",
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(GenericAPIView):
    """User authentication view.

    We're using custom one because Knox using basic auth as default
    authorization method.

    """

    permission_classes = (permissions.AllowAny,)
    authentication_classes = ()
    serializer_class = serializers.AuthTokenSerializer

    def post(self, request: Request, *args, **kwargs):
        """Login user and get auth token with expiry."""
        credentials_serializer = self.get_serializer(
            data=request.data,
        )
        credentials_serializer.is_valid(raise_exception=True)
        user = credentials_serializer.validated_data["user"]
        login(request, user)
        tokens_pair = issue_pair(
            request.user,
            user_agent=get_user_agent(request),
            ip=get_client_ip(request),
        )
        return Response(
            data=serializers.JWTSerializer(
                tokens_pair,
            ).data,
            status=status.HTTP_200_OK,
        )


class LogoutView(GenericAPIView):
    """User logout view."""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, *args, **kwargs):
        """Logout user and revoke token."""
        claims = decode_token(request.auth)
        revoke_by_jti(claims["jti"])
        return Response({"detail": "Logged out"}, status=status.HTTP_200_OK)


class LogoutAllView(GenericAPIView):
    """User logout view."""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, *args, **kwargs):
        """Logout user and revoke all tokens."""
        revoke_all_for_user(request.user)
        return Response(
            {
                "detail": "Logged out all tokens",
            },
            status=status.HTTP_200_OK,
        )


class DeactivateUserView(GenericAPIView):
    """Soft user deactivation view."""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request: Request, *args, **kwargs):
        """Deactivate account and revoke all tokens."""
        user = request.user
        user.is_active = False
        revoke_all_for_user(user)
        user.save()
        return Response(
            data={
                "detail": "Account deactivated successfully",
            },
            status=status.HTTP_200_OK,
        )


class RefreshView(GenericAPIView):
    """Exchange refresh token view."""

    permission_classes = [permissions.AllowAny]
    authentication_classes = ()
    serializer_class = serializers.RefreshExchangeSerializer

    def post(self, request, *args, **kwargs):
        """Exchange refresh token for new access and refresh."""
        refresh_serializer = self.get_serializer(request.data)
        refresh_serializer.is_valid(raise_exception=True)
        refresh_token = refresh_serializer.validated_data["token"]
        try:
            tokens_pair = rotate_refresh(
                refresh_token,
                user_agent=get_user_agent(request),
                ip=get_client_ip(request),
            )
        except jwt.InvalidTokenError as error:
            return Response(
                {
                    "error": "Token error {error}".format(
                        error=str(error),
                    ),
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            data=serializers.JWTSerializer(
                tokens_pair,
            ).data,
            status=status.HTTP_200_OK,
        )


def get_user_agent(request: Request) -> str:
    """Return user agent from request."""
    return request.META.get("HTTP_USER_AGENT", "")


def get_client_ip(request: Request) -> str:
    """Get request ip address from request."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip
