from django.urls import path
from .views import (
    SignUpView,
    home,
    create_group,
    group_detail,
    group_ocr,
    delete_note,
    favorites,
    archived,
    toggle_favorite,
    toggle_archive,
    delete_group,
)

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("home/", home, name="home"),
    path("", home, name="home"),
    path("create-group/", create_group, name="create_group"),
    path("group/<int:group_id>/", group_detail, name="group_detail"),
    path("group/<int:group_id>/delete/", delete_group, name="delete_group"),
    path("group/<int:group_id>/ocr/", group_ocr, name="group_ocr"),
    path("note/<int:note_id>/delete/", delete_note, name="delete_note"),
    path("favorites/", favorites, name="favorites"),
    path("archived/", archived, name="archived"),
    path("note/<int:note_id>/favorite/", toggle_favorite, name="toggle_favorite"),
    path("note/<int:note_id>/archive/", toggle_archive, name="toggle_archive"),
]