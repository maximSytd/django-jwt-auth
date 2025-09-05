from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class CanViewBooks(BasePermission):
    """Permission to view books for user."""

    def has_permission(self, request: Request, view):
        """Return bool of the user has permission."""
        return request.user.is_authenticated and request.user.has_perm(
            "books.can_view_books",
        )