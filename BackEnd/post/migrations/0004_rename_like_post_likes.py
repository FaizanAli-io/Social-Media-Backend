# Generated by Django 5.0.1 on 2024-02-08 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_post_like_count_like_post_like'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='like',
            new_name='likes',
        ),
    ]