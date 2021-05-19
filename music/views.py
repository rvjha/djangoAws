from django.shortcuts import redirect, render
from django.http import request, response
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import subscribe_func

# Create your views here.
def home(request):
    if request.session.has_key("uId"):
        userData = {
            "uId": request.session["uId"],
            "uNm": request.session["uNm"],
        }
        return render(
            request,
            "pages/home.html",
            {"pageName": "Home | Music app", "user": userData},
        )
    else:
        return render(request, "pages/login.html", {"pageName": "login | Music app"})

def error_404(request, exception=None):
    data = {}
    return render(request, "pages/error_404.html", data)
