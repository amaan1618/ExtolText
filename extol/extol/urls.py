from django.contrib import admin
from django.urls import path, include
from django.views.generic.base import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),  # login/logout
    path("", RedirectView.as_view(pattern_name="login", permanent=False)),  # home → login
    path("accounts/", include("main.urls")),  # replace 'your_app' with your app name
]
