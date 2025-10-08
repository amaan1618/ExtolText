from django.urls import path
from .views import SignUpView, home, create_group, group_detail

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("home/", home, name="home"),
    path("", home, name="home"),
    path("create-group/", create_group, name="create_group"),
    path("group/<int:group_id>/", group_detail, name="group_detail"),
]
