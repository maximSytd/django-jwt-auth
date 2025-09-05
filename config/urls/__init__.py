from django.contrib import admin
from django.urls import path

from apps.core.views import IndexView
from .api_versions import urlpatterns as api_urlpatterns
from .debug import urlpatterns as debug_urlpatterns


urlpatterns = [
    path(
        "",
        IndexView.as_view(),
        name="index",
    ),
]

urlpatterns += (
        path(
            "admin/",
            admin.site.urls,
        ),
    )


urlpatterns += api_urlpatterns
urlpatterns += debug_urlpatterns
