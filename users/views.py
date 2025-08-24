# users/views.py
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required

from .forms import UserRegisterForm, UserUpdateForm
from movies.models import Movie, Booking

def home(request):
    movies = Movie.objects.all()
    return render(request, "home.html", {"movies": movies})

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
            return redirect("profile")
    else:
        form = UserRegisterForm()
    return render(request, "users/register.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("/")
    else:
        form = AuthenticationForm()
    return render(request, "users/login.html", {"form": form})

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)

    user_bookings = Booking.objects.filter(email=request.user.email)
    booked_names = user_bookings.values_list('movie', flat=True)
    recommended_movies = Movie.objects.exclude(name__in=booked_names).order_by('-rating')[:5]
    if not recommended_movies.exists():
        recommended_movies = Movie.objects.order_by('-rating')[:5]

    context = {
        "u_form": u_form,
        "bookings": user_bookings,
        "user_bookings": user_bookings.exists(),
        "recommended_movies": recommended_movies,
    }
    return render(request, "users/profile.html", context)

@login_required
def reset_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = PasswordChangeForm(user=request.user)
    return render(request, "users/reset_password.html", {"form": form})
