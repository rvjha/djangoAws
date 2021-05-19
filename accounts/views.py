from json.decoder import JSONDecoder
from django.http import request, response
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import (
    get_table,
    create_table,
    get_users_data,
    register_user,
    subscribe_song,
    upload_data,
    login_user,
    get_table_data,
    query_data,
    create_bucket,
    get_sub_list,
    collect_images_data,
)
from django.contrib.auth import logout, authenticate
import re
import json


# Create your views here.

# register page
def reg(request):
    if request.method == "GET":
        if request.session.has_key("uId"):
            return redirect("profile")
        else:
            return render(
                request, "pages/reg.html", {"pageName": "Register | Music app"}
            )


# register user ajax request
def register_req(request):
    if request.method == "POST":
        data = {
            "nm": request.POST.get("name"),
            "email": request.POST.get("email"),
            "ps": request.POST.get("pass"),
        }
        msg = []
        for element in data:
            if data[element] == None:
                msg.push(element)

            if len(msg):
                return HttpResponse("false")
            else:
                response = register_user(data)
            return HttpResponse(response)


# login user
def login(request):
    if request.method == "GET":
        if request.session.has_key("uId"):
            return redirect("profile")
        else:
            return render(
                request, "pages/login.html", {"pageName": "Login | Music app"}
            )


# login user ajax request
def login_req(request):
    if request.method == "POST":
        data = {
            "email": request.POST.get("email"),
            "ps": request.POST.get("pass"),
        }
        msg = []
        for element in data:
            if data[element] == None:
                msg.push(element)

        if len(msg):
            return HttpResponse("false")
        else:
            response = login_user(data)
            if response:
                request.session["uId"] = response["email"]
                request.session["uNm"] = response["user_name"]
                return redirect("profile")
            else:
                return HttpResponse(response)


# user profile
def profile(request):
    if request.session.has_key("uId"):
        userData = {
            "uId": request.session["uId"],
            "uNm": request.session["uNm"],
        }
        return render(
            request,
            "pages/profile.html",
            {"pageName": "Profile | Music app", "user": userData},
        )
    else:
        return redirect("/")


# user logout
def log_out(request):
    if request.session.has_key("uId"):
        del request.session["uId"]
    else:
        logout(request)
    return redirect("login")


# ======================== admin functions ===================================
# admin login
def admin(request):
    # return render(request, "pages/admin.html", {"pageName": "Admin | Music app"})
    if request.session.has_key("uId"):
        if request.session["uId"] == "rominaniraula.111@gmail.com":
            userData = {
                "uId": request.session["uId"],
                "uNm": request.session["uNm"],
            }
            return render(
                request,
                "pages/admin.html",
                {"pageName": "Admin | Music app", "user": userData},
            )
        else:
            return redirect("/")
    else:
        return redirect("/login")


# get table
def check_table(request):
    if request.method == "POST":
        reqData = request.POST.get("action")
        ty = request.POST.get("type")
        tb = request.POST.get("table")
        if reqData == "get_table":
            response = get_table(ty, tb)
            if response == False:
                return HttpResponse("false")
            else:
                return HttpResponse("true")
        else:
            return HttpResponse("false")
    else:
        return redirect("/")


# create music class
def build_table(request):
    pMethod = request.method
    pAction = request.POST.get("action")
    if (
        (pMethod == "POST")
        & (pAction == "create_data")
        & request.session.has_key("uId")
    ):
        tb = request.POST.get("table")
        ty = request.POST.get("type")
        response = get_table(ty, tb)
        if response == False:
            if ty == "table":
                table = create_table(ty, tb)
                if table["TableDescription"]["TableStatus"] == "CREATING":
                    return HttpResponse("true")
                else:
                    return HttpResponse("false")
        else:
            return HttpResponse("true")
    else:
        return redirect("/")


def build_bucket(request):
    pMethod = request.method
    pAction = request.POST.get("action")
    if (
        (pMethod == "POST")
        & (pAction == "create_data")
        & request.session.has_key("uId")
    ):
        tb = request.POST.get("table")
        ty = request.POST.get("type")
        response = get_table(ty, tb)
        if response == False:
            if ty == "s3":
                table = create_bucket(ty, tb)
                return HttpResponse(table)
            else:
                return HttpResponse("false")
        else:
            return HttpResponse("false")
    else:
        return HttpResponse("false")


# collect images from json file image urls
def collect_image_data(request):
    if request.method == "POST":
        reqData = request.POST.get("action")
        if reqData == "collect_images":
            response = collect_images_data()
            return HttpResponse(response)
        else:
            return HttpResponse("false")
    else:
        return HttpResponse("false")


# get all the users
def get_users(request):
    if request.session.has_key("uId"):
        if request.method == "POST":
            reqData = request.POST.get("action")
            if reqData == "get_users":
                items = get_users_data()
                return HttpResponse(json.dumps(items), content_type="application/json")
            else:
                return HttpResponse("Invalid Request")
        else:
            return redirect("/")
    else:
        return HttpResponse("not authroise")


# upload json file
def upload_music_data(request):
    if request.session.has_key("uId"):
        if request.method == "POST":
            data = json.loads(request.body)
            response = get_table("table", "music")
            if response:
                response = upload_data(data)
                return HttpResponse(response)
            else:
                return HttpResponse("Table not exists")
        else:
            return redirect("/")
    else:
        return HttpResponse("not authroise")


# get music data
def get_music_data(request):
    if request.method == "POST":
        reqData = request.POST.get("action")
        if reqData == "get_music_data":
            response = get_table("table", "music")
            if response:
                response = get_table_data("music")
                return HttpResponse(
                    json.dumps(response), content_type="application/json"
                )
            else:
                return HttpResponse("Table not exists")
        else:
            return HttpResponse("Invalid Request")
    else:
        return redirect("/")


# query data
def query(request):
    if request.method == "GET":
        userData = {
            "uId": request.session["uId"],
            "uNm": request.session["uNm"],
        }
        return render(
            request,
            "pages/query.html",
            {"pageName": "Admin | Music app", "user": userData},
        )
    elif request.method == "POST":
        data = request.POST
        response = query_data(data)
        return HttpResponse(json.dumps(response), content_type="application/json")


# subscribe
def subscribe(request):
    if request.session.has_key("uId"):
        songId = request.POST.get("sId")
        artist = request.POST.get("artist")
        data = {"uId": request.session["uId"], "songId": songId, "artist":artist}
        return HttpResponse(subscribe_song(data))
    else:
        return HttpResponse("require_loign")


def get_sub_data(request):
    if request.session.has_key("uId"):
        uId = request.session["uId"]
        data = get_sub_list(uId)
        return HttpResponse(json.dumps(data), content_type="application/json")
    else:
        return HttpResponse("require_loign")


# ==================================================== validate email and password ========================================
# def check(email):
#     if re.search(regex, email):
#         return True
#     else:
#         return False


# def password_check(passwd):
# SpecialSym = ["$", "@", "#", "%"]
# val = True

# if len(passwd) < 6:
#     val = False
#     return "length should be at least 6"

# if len(passwd) > 20:
#     val = False
#     return "length should be not be greater than 8"

# if not any(char.isdigit() for char in passwd):
#     val = False
#     return "Password should have at least one numeral"

# if not any(char.isupper() for char in passwd):
#     val = False
#     return "Password should have at least one uppercase letter"

# if not any(char.islower() for char in passwd):
#     val = False
#     return "Password should have at least one lowercase letter"

# if not any(char in SpecialSym for char in passwd):
#     val = False
#     return "Password should have at least one of the symbols $@#"
# if val:
#     return val
