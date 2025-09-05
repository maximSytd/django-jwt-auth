from django.conf import settings
from django.contrib.auth import (
    authenticate,
    get_user_model,
)
from django.contrib.auth.hashers import make_password
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from libs.open_api.serializers import OpenApiSerializer

from ..serializers import UserSerializer

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    """Custom registry serializer."""

    password = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
    )
    password2 = serializers.CharField(
        write_only=True,
        min_length=8,
        max_length=128,
    )

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "password2"]

    def validate(self, attrs: dict):
        if attrs["password"] != attrs["password2"]:
            raise ValidationError({"password2": "Passwords do not match"})

        if User.objects.filter(email__iexact=attrs["email"]).exists():
            raise ValidationError(
                {
                    "email": "User with this email already exists",
                },
            )

        return attrs

    def create(self, validated_data: dict):
        password = validated_data.pop("password")
        validated_data.pop("password2", None)
        user = User(
                username=validated_data["email"],
                email=validated_data["email"],
                first_name=validated_data.get("first_name", ""),
                last_name=validated_data.get("last_name", ""),
                is_active=True,
            )
        user.password = make_password(password)
        user.save()
        return user

    def update(self, instance, validated_data) -> None:
        """Escape warning."""


class AuthTokenSerializer(serializers.Serializer):
    """Custom auth serializer to use email instead of username.

    Copied form rest_framework.authtoken.serializers.AuthTokenSerializer

    """

    email = serializers.CharField(
        write_only=True,
        required=True,
    )
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
        write_only=True,
        required=True,
    )

    def validate(self, attrs: dict) -> dict:
        """Authenticate with input data."""
        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"),
            email=email,
            password=password,
        )

        # The authenticate call simply returns None for is_active=False
        # users. (Assuming the default ModelBackend authentication
        # backend.)
        if not user:
            msg = _("Unable to log in with provided credentials.")
            raise serializers.ValidationError(msg, code="authorization")

        attrs["user"] = user
        return attrs

    def create(self, validated_data: dict) -> None:
        """Escape warning."""

    def update(self, instance, validated_data) -> None:
        """Escape warning."""


class JWTSerializer(OpenApiSerializer):
    """Auth jwt token for entire app."""

    access = serializers.CharField()
    access_expiry = serializers.IntegerField(
        help_text=f"Token expires in {settings.JWT_SETTINGS['ACCESS_TTL']}",
    )
    refresh = serializers.CharField()
    refresh_expiry = serializers.IntegerField(
        help_text=f"Token expires in {settings.JWT_SETTINGS['REFRESH_TTL']}",
    )
    user = UserSerializer()


class RefreshExchangeSerializer(serializers.Serializer):
    """Serializer for refresh token exchange to new pair."""

    token = serializers.CharField(
        write_only=True,
        required=True,
    )
