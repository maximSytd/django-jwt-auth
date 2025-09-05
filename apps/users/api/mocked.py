from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework import permissions, status
from rest_framework.response import Response

FAKE_DB = [
    {
        "id": 1,
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "price": 450,
        "amount": 12,
    },
    {
        "id": 2,
        "title": "1984",
        "author": "Джордж Оруэлл",
        "price": 380,
        "amount": 8,
    },
    {
        "id": 3,
        "title": "Преступление и наказание",
        "author": "Фёдор Достоевский",
        "price": 520,
        "amount": 15,
    },
    {
        "id": 4,
        "title": "Гарри Поттер и философский камень",
        "author": "Джоан Роулинг",
        "price": 670,
        "amount": 20,
    },
    {
        "id": 5,
        "title": "Маленький принц",
        "author": "Антуан де Сент-Экзюпери",
        "price": 290,
        "amount": 25,
    },
]

class MockedDataSerializer(serializers.Serializer):
    """Serializers for mocked data from `FAKE_DB`."""

    id = serializers.IntegerField()
    title = serializers.CharField()
    author = serializers.CharField()
    price = serializers.IntegerField()
    amount = serializers.IntegerField()


class MockView(GenericAPIView):
    """Mocked data view."""

    serializer_class = MockedDataSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """Return mocked data for tests."""
        serializer = self.get_serializer(data=FAKE_DB, many=True)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
