from apps.core.api.serializers import ModelBaseSerializer
from ..models import Book

class BookSerializer(ModelBaseSerializer):
    """Serializer for representing `Book`."""

    class Meta:
        model = Book
        fields = [
            "id",
            "title",
            "author",
        ]
