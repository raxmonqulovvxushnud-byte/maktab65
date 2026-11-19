
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.db import transaction

from .models import SchoolInfo, News, Gallery, UserProfile

User = get_user_model()


def home(request):
    school = SchoolInfo.objects.first()
    news = News.objects.all()[:6]
    gallery = Gallery.objects.all()[:8]

    return render(request, "index.html", {
        "school": school,
        "news": news,
        "gallery": gallery,
    })


def register(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        role = request.POST.get("role")
        grade = request.POST.get("grade", "").strip()
        subject = request.POST.get("subject", "").strip()

        if role not in ["student", "teacher"]:
            messages.error(request, "Foydalanuvchi turini tanlang.")
        elif role == "student" and grade not in [
            f"{i}-{letter}" for i in range(1, 12)
            for letter in ["A", "B", "D"]
        ]:
            messages.error(request, "Sinfni to‘g‘ri tanlang.")
        elif role == "teacher" and not subject:
            messages.error(request, "Fan nomini kiriting.")
        elif form.is_valid():
            with transaction.atomic():
                user = form.save()
                UserProfile.objects.create(
                    user=user,
                    role=role,
                    grade=grade if role == "student" else "",
                    subject=subject if role == "teacher" else "",
                    is_approved=(role == "student"),
                )

            messages.success(
                request,
                "Ro‘yxatdan o‘tish muvaffaqiyatli! Endi tizimga kiring."
            )
            return redirect("login")

    else:
        form = UserCreationForm()

    return render(request, "register.html", {"form": form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect("dashboard")

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "login.html", {"form": form})


@login_required
def dashboard(request):
    try:
        profile = request.user.profile
    except UserProfile.DoesNotExist:
        messages.error(request, "Profil ma'lumotlari topilmadi.")
        return redirect("home")

    return render(request, "dashboard.html", {"profile": profile})


@login_required
def user_logout(request):
    logout(request)
    return redirect("home")
