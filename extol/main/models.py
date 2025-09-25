from django.contrib.auth.models import User
from django.db import models

class Group(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.name

class Note(models.Model):
    group = models.ForeignKey(Group,on_delete=models.CASCADE)
    title=models.CharField(max_length=100)
    text=models.TextField()
    created = models.DateTimeField(auto_now_add=True)
