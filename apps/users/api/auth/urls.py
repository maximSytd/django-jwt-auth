from django.urls import path

from . import views

urlpatterns = [
    path(
        "register/",
        views.RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        views.LoginView.as_view(),
        name="login",
    ),
    path(
        "logout/",
        views.LogoutView.as_view(),
        name="logout",
    ),
    path(
        "logout-all/",
        views.LogoutAllView.as_view(),
        name="logout-all",
    ),
    path(
        "deactivate/",
        views.DeactivateUserView.as_view(),
        name="deactivate",
    ),
    path(
        "refresh/",
        views.RefreshView.as_view(),
        name="refresh",
    ),
]
