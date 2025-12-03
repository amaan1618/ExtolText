from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
    path("accounts/", include("main.urls")),  # your app routes
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),  # root → login
]