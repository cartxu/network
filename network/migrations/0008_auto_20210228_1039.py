# Generated by Django 3.1.5 on 2021-02-28 09:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0007_follow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='follow',
            name='follow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_follow', to='network.profile'),
        ),
        migrations.AlterField(
            model_name='follow',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_following', to=settings.AUTH_USER_MODEL),
        ),
    ]
