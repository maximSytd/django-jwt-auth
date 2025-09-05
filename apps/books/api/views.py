from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response

from .serializers import BookSerializer
from .permissions import CanViewBooks

FAKE_DB = [
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
    },
    {
        "title": "1984",
        "author": "Джордж Оруэлл",
    },
    {
        "title": "Преступление и наказание",
        "author": "Фёдор Достоевский",
    },
    {
        "title": "Гарри Поттер и философский камень",
        "author": "Джоан Роулинг",
    },
    {
        "title": "Маленький принц",
        "author": "Антуан де Сент-Экзюпери",
    },
]

class MockBookView(GenericAPIView):
    """Mocked data of books view."""

    serializer_class = BookSerializer
    permission_classes = [CanViewBooks]

    def get(self, request, *args, **kwargs):
        """
        Return mocked data for tests.

        Required can_view_books permission for user.
        """
        serializer = self.get_serializer(data=FAKE_DB, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
