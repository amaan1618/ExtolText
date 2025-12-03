import sys
import os
from PIL import Image
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Group, Note

# Path to external OCR project
OCR_PATH = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "ocrproject")
)

if OCR_PATH not in sys.path:
    sys.path.insert(0, OCR_PATH)

# import OCR utils
from ocr_utils import run_ocr, run_ocr_pdf


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


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


@login_required
def delete_group(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    group.delete()
    messages.success(request, "Group deleted successfully.")
    return redirect("home")


@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    notes = Note.objects.filter(group=group)
    return render(request, "main/group_detail.html", {"group": group, "notes": notes})

@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.group.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this note.")
    group_id = note.group.id
    note.delete()
    return redirect("group_detail", group_id=group_id)

@login_required
def group_ocr(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)

    if request.method == "POST":
        file = request.FILES.get("image")
        title = request.POST.get("title") or "Scanned Note"

        if not file:
            messages.error(request, "Please upload an image or PDF file.")
            return redirect("group_detail", group_id=group.id)

        try:
            ext = file.name.lower().split(".")[-1]

            if ext == "pdf":
                extracted_text = run_ocr_pdf(file.read())
            else:
                img = Image.open(file)
                extracted_text = run_ocr(img)

            if extracted_text.strip():
                Note.objects.create(group=group, title=title, text=extracted_text.strip())
                messages.success(request, "OCR note created successfully.")
            else:
                messages.error(request, "OCR returned no usable text.")

        except Exception as e:
            messages.error(request, f"OCR failed: {e}")

        return redirect("group_detail", group_id=group.id)

    return redirect("group_detail", group_id=group.id)

@login_required
def favorites(request):
    notes = Note.objects.filter(group__user=request.user, is_favorite=True, is_archived=False)
    return render(request, "main/favorites.html", {"notes": notes})

@login_required
def archived(request):
    notes = Note.objects.filter(group__user=request.user, is_archived=True)
    return render(request, "main/archived.html", {"notes": notes})

@login_required
def toggle_favorite(request, note_id):
    note = get_object_or_404(Note, id=note_id, group__user=request.user)
    note.is_favorite = not note.is_favorite
    note.save()
    return redirect("group_detail", group_id=note.group.id)

@login_required
def toggle_archive(request, note_id):
    note = get_object_or_404(Note, id=note_id, group__user=request.user)
    note.is_archived = not note.is_archived
    note.save()
    return redirect("group_detail", group_id=note.group.id)
