from django.urls import path

from rest_framework.routers import DefaultRouter

from . import views, mocked

router = DefaultRouter()
router.register(r"", views.UsersViewSet, basename="user")
urlpatterns = [
    path(
        "mocked/",
        mocked.MockView().as_view(),
        name="mocked",
    ),
]
urlpatterns += router.urls
