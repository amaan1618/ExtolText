from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import Group, Note

# Home page (after login)
@login_required
def home(request):
    return render(request, "main/mhome.html")  # your HTML file

# Signup view
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

def create_group(request):
    if request.method == "POST":
        title = request.POST.get("title")
        Group.objects.create(title=title)
        return redirect("task_list")  # change to wherever you want to go
    return render(request, "main/mhome.html")

@login_required
def home(request):
    groups = Group.objects.filter(user=request.user)
    return render(request, "main/mhome.html", {"groups": groups})

@login_required
def create_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Group.objects.create(user=request.user, name=name)
        return redirect("home")

def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    notes = Note.objects.filter(group=group)
    return render(request, "main/group_detail.html", {"group": group, "notes": notes})