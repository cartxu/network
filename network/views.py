import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

from .models import *
from .forms import *


def index(request):
    posts = Post.objects.all().order_by('-timestamp')
    paginator = Paginator(posts, 10) 
    #mostrar 10 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    profiles = Profile.objects.all()
 
    #Publicar posts desde la página principal:
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        form = PostForm(request.POST)
        if request.method == "POST":
            
            if form.is_valid():
                post = form.save(commit=False)
                post.user = request.user
                post.save()
                return HttpResponseRedirect(reverse('index'))
            else:
                return render(request, "network/index.html", {
                    "profile": profile,
                    "form": form,
                    "posts": posts,
                    "page_obj": page_obj,
                    "profiles": profiles
                })
    else:
        return render(request, "network/index.html", {
            "posts": posts,
            "page_obj": page_obj,
            "profiles": profiles
        })


    return render(request, "network/index.html", {
                    "profile": profile,
                    "form": form,
                    "posts": posts,
                    "page_obj": page_obj,
                    "profiles": profiles
                })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            profile = Profile.objects.get(user=request.user)
            if profile:
                return HttpResponseRedirect(reverse("index"))
            else:
                return HttpResponseRedirect(reverse("bio"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")

def bio(request):
    user = request.user
    form = ProfileForm(request.POST)
    if request.method == "POST":
        
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = user
            profile.save()
            return HttpResponseRedirect(reverse("index"))
        
    return render(request, "network/bio.html", {
        "form": form
    })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("bio"))
    else:
        return render(request, "network/register.html")

#función que recibe el nombre del usuario y carga su pagina
def profile(request, username):
    user = User.objects.get(username=username)
    posts = Post.objects.filter(user=user).order_by('-timestamp')
    profile = Profile.objects.get(user=user)

    #mostrar 10 posts por página
    paginator = Paginator(posts, 10) 
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    follow_user = request.user
    

    if request.method == "POST" and request.POST.get("Follow"):
        profile.follower.add(follow_user)
        profile.save()

        following = Profile.objects.get(user=request.user)
        following.following.add(user)
        profile.save()

        return HttpResponseRedirect(reverse('profile', args=(username,)))

    if request.method == "POST" and request.POST.get("Unfollow"):
        profile.follower.remove(follow_user)
        profile.save()

        following = Profile.objects.get(user=request.user)
        following.following.remove(user)
        profile.save()

        return HttpResponseRedirect(reverse('profile', args=(username,)))

    return render(request, "network/profile.html", {
        "profile": profile,
        "posts": posts,
        "user": user,
        "page_obj": page_obj
    })

@csrf_exempt
@login_required
# Función para borrar posts 
def delete(request):

    if request.method == "POST":
        try:
            post_id = request.POST.get('id')
            post = Post.objects.get(id=post_id)
            post.delete()
            return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)
   
    

@login_required
def following(request):
    #obtenemos el usuario que está logueado
     
    profile = Profile.objects.get(user=request.user)
    following = Profile.objects.get(user=request.user).following.all()
    user_follow = Profile.objects.get(user=request.user).following
    #obtenemos los follows del usuario que está logueado
    posts = Post.objects.filter(user__in=following).order_by('-timestamp')
 
    
    # Paginación: 
    paginator = Paginator(posts, 10) #mostrar 10 posts por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    

    return render(request, "network/following.html", {
                    "following": following,
                    "profile": profile,
                    "posts": posts,
                    "page_obj": page_obj,
                    "user_follow": user_follow
                })


@csrf_exempt
@login_required
#Función para editar posts mediante Javascript
def edit(request):

    if request.method == "POST":
        post_id = request.POST.get('id')
        post_body = request.POST.get('post')
        try:
            post = Post.objects.get(id=post_id)
            post.body = post_body
            post.save()
            return JsonResponse({}, status=201)
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)

@csrf_exempt
@login_required
def like(request):
#función que recibe la petición de JS por fetch y añade o elimina like
    if request.method == "POST":
        post_id = request.POST.get('id')
        try:
            post = Post.objects.get(id=post_id)
            if request.user in post.like.all():
                post.like.remove(request.user)
                post.save()
                count = post.like.count()
                return JsonResponse({'count': count, "status":201})
            else:
                post.like.add(request.user)
                post.save()
                count = post.like.count()
                return JsonResponse({'count': count, "status":201})
        except:
            return JsonResponse({}, status=404)

    return JsonResponse({}, status=400)


@login_required
def unlike(request, post_id):
    post = Post.objects.get(id=post_id)
    user = User.objects.get(username=request.user)

    post.like.remove(user)
    post.save

    return HttpResponseRedirect(reverse("index"))


def users(request):
    users = User.objects.all()
    profile = Profile.objects.all()

    return render(request, "network/users.html", {
        "users": users,
        "profile": profile
    })