from django.urls import path
from .views import SignUpView, home

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("home/", home, name="home"),
]
