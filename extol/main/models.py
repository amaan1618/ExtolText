from django.contrib.auth.models import User
from django.db import models

class Group(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="custom_groups"  # Avoids conflict with auth.User.groups
    )
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Group"
        verbose_name_plural = "Groups"


class Note(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="notes"
    )
    title = models.CharField(max_length=100)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    is_favorite = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"