import sys
import os
from io import BytesIO
from PIL import Image
import tempfile

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden
from .models import Group, Note

# Add OCR project folder to Python path
OCR_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "ocrproject")
OCR_PATH = os.path.abspath(OCR_PATH)
if OCR_PATH not in sys.path:
    sys.path.insert(0, OCR_PATH)

from ocr_utils import run_full_ocr  # <- your OCR function

# ================== Signup view ==================
class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"

# ================== Home view ==================
@login_required
def home(request):
    groups = Group.objects.filter(user=request.user)
    return render(request, "main/mhome.html", {"groups": groups})

# ================== Create group ==================
@login_required
def create_group(request):
    if request.method == "POST":
        name = request.POST.get("name")
        if name:
            Group.objects.create(user=request.user, name=name)
        return redirect("home")

# ================== Group detail ==================
@login_required
def group_detail(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)
    notes = Note.objects.filter(group=group)
    return render(request, "main/group_detail.html", {"group": group, "notes": notes})

# ================== Delete note ==================
@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.group.user != request.user:
        return HttpResponseForbidden("You don't have permission to delete this note.")
    group_id = note.group.id
    note.delete()
    return redirect("group_detail", group_id=group_id)

# ================== OCR view ==================
@login_required
def group_ocr(request, group_id):
    group = get_object_or_404(Group, id=group_id, user=request.user)

    if request.method == "POST":
        image_file = request.FILES.get("image")
        title = request.POST.get("title") or "Scanned Note"

        if not image_file:
            messages.error(request, "Please upload an image or PDF file.")
            return redirect("group_detail", group_id=group.id)

        try:
            ext = image_file.name.split(".")[-1].lower()
            if ext == "pdf":
                from pdf2image import convert_from_bytes
                images = convert_from_bytes(image_file.read())
                all_text = ""
                for img in images:
                    text = run_full_ocr(img)
                    all_text += text + "\n"
            else:
                pil_img = Image.open(image_file)
                all_text = run_full_ocr(pil_img)

            if all_text.strip():
                Note.objects.create(group=group, title=title, text=all_text)
                messages.success(request, "OCR note created successfully.")
            else:
                messages.error(request, "OCR returned no usable text.")

        except Exception as e:
            messages.error(request, f"OCR failed: {str(e)}")

        return redirect("group_detail", group_id=group.id)

    return redirect("group_detail", group_id=group.id)

# ================== Favorites tab ==================
@login_required
def favorites(request):
    notes = Note.objects.filter(group__user=request.user, is_favorite=True, is_archived=False)
    return render(request, "main/favorites.html", {"notes": notes})

# ================== Archived tab ==================
@login_required
def archived(request):
    notes = Note.objects.filter(group__user=request.user, is_archived=True)
    return render(request, "main/archived.html", {"notes": notes})

# ================== Toggle favorite ==================
@login_required
def toggle_favorite(request, note_id):
    note = get_object_or_404(Note, id=note_id, group__user=request.user)
    note.is_favorite = not note.is_favorite
    note.save()
    return redirect("group_detail", group_id=note.group.id)

# ================== Toggle archive ==================
@login_required
def toggle_archive(request, note_id):
    note = get_object_or_404(Note, id=note_id, group__user=request.user)
    note.is_archived = not note.is_archived
    note.save()
    return redirect("group_detail", group_id=note.group.id)
