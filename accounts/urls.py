from django.urls import path
from . import views

urlpatterns = [
    # user urls
    path("", views.profile, name="profile"),
    path("profile", views.profile, name="profile"),
    path("register", views.reg, name="reg"),
    path("register_req", views.register_req, name="register_req"),
    path("login", views.login, name="login"),
    path("login_req", views.login_req, name="login_req"),
    path("logout", views.log_out, name="logout"),
    path("admin", views.admin, name="admin"),
    # databse urls
    path("query", views.query, name="query"),
    path("get_music_data", views.get_music_data, name="get_music_data"),
    path("check_table", views.check_table, name="check_table"),
    path("build_table", views.build_table, name="build_table"),
    path("build_bucket", views.build_bucket, name="build_bucket"),
    path("upload_music_data", views.upload_music_data, name="upload_music_data"),
    path("collect_image_data", views.collect_image_data, name="collect_image_data"),
    path("get_users", views.get_users, name="get_users"),
    path("subscribe", views.subscribe, name="subscribe"),
    path("get_sub_data", views.get_sub_data, name="get_sub_data"),

]
