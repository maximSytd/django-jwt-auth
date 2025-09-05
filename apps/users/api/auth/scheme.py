from django.utils.translation import gettext_lazy as _

from drf_spectacular.extensions import OpenApiAuthenticationExtension
from drf_spectacular.utils import extend_schema, extend_schema_view

from libs.open_api.extend_schema import fix_api_view_warning
from libs.open_api.serializers import DetailSerializer

from . import serializers, views


class JWTTokenScheme(OpenApiAuthenticationExtension):
    """Scheme to describe jwt token auth scheme."""

    target_class = "apps.users.authentication.JWTAuthentication"
    name = "JWTAuth"

    def get_security_definition(self, auto_schema) -> dict[str, str]:
        """Define security definition."""
        return {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": _(
                "JWT token-based authentication with required prefix",
            ),
        }


fix_api_view_warning(views.RegisterView)
fix_api_view_warning(views.LoginView)
fix_api_view_warning(views.LogoutView)
fix_api_view_warning(views.LogoutAllView)
fix_api_view_warning(views.DeactivateUserView)
fix_api_view_warning(views.RefreshView)

extend_schema_view(
    post=extend_schema(
        request=serializers.RegisterSerializer,
        responses=DetailSerializer,
    ),
)(views.RegisterView)

extend_schema_view(
    post=extend_schema(
        request=serializers.AuthTokenSerializer,
        responses=serializers.JWTSerializer,
    ),
)(views.LoginView)

extend_schema_view(
    post=extend_schema(
        responses=DetailSerializer,
    ),
)(views.LogoutView)

extend_schema_view(
    post=extend_schema(
        responses=DetailSerializer,
    ),
)(views.LogoutAllView)

extend_schema_view(
    post=extend_schema(
        responses=DetailSerializer,
    ),
)(views.DeactivateUserView)

extend_schema_view(
    post=extend_schema(
        responses=serializers.JWTSerializer,
    ),
)(views.RefreshView)
