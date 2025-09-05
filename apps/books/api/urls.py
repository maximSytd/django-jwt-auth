from django.urls import path
from .views import MockBookView

urlpatterns = [
    path(
        "mock-books/",
        MockBookView.as_view(),
        name="mock-books",
    ),
]
