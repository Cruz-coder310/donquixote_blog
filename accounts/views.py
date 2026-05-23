from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

from .forms import CreationOfUser


@login_required
def dashboard(request):
    return render(request, "dashboard.html", {})


def registration(request):
    if request.method == "POST":
        form = CreationOfUser(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User = get_user_model()
            User.objects.create_user(
                username=cd["username"],
                email=cd["email"],
                password=cd["password1"],
            )
            return redirect("home")

    else:
        form = CreationOfUser()

    return render(request, "registration/register.html", {"form": form})
