from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_profile")
    bio = models.TextField()
    avatar = models.CharField(max_length=200, default=None, blank=True, null=True)
    follower = models.ManyToManyField(User, blank=True, related_name="follower_user")
    following = models.ManyToManyField(User,  blank=True, related_name="following_user")

    def __str__(self):
        return f"{self.user}"


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_posts")
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    like = models.ManyToManyField(User, blank=True, related_name="like")
    

    def __str__(self):
        return f"{self.user}"

    