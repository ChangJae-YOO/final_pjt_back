# Generated by Django 3.2.12 on 2023-05-18 07:49

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('movies', '0005_auto_20230518_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='user_likes',
            field=models.ManyToManyField(related_name='comments_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
