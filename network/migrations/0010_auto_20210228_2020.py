# Generated by Django 3.1.5 on 2021-02-28 19:20

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0009_follow_posts'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='like',
            field=models.ManyToManyField(blank=True, related_name='like', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='follower',
            field=models.ManyToManyField(blank=True, related_name='follower_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(blank=True, related_name='following_user', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
    ]
