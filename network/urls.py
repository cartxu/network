
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("user/<str:username>", views.profile, name="profile"),
    path("delete/", views.delete, name="delete"),
    path("following", views.following, name="following"),
    path("bio", views.bio, name="bio"),
    path("users", views.users, name="users"),

    # API ROUTE 
    path("like/", views.like, name="like"),
    path("edit/", views.edit, name="edit")
]
