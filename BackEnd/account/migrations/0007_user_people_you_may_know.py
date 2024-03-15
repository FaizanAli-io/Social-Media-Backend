# Generated by Django 5.0.3 on 2024-03-14 17:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0006_alter_user_friends"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="people_you_may_know",
            field=models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
        ),
    ]