from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **options):

        get_user_model().objects.create_superuser(
            email="admin@example.com",
            name="The Admin",
            password="123",
            is_active=True,
        )

        get_user_model().objects.create_user(
            email="faizan@example.com",
            name="Faizan Ali",
            password="123",
            is_active=True,
        )

        get_user_model().objects.create_user(
            email="farooq@example.com",
            name="Farooq Ahmed",
            password="123",
            is_active=True,
        )

        get_user_model().objects.create_user(
            email="hassan@example.com",
            name="Hassan Tariq",
            password="123",
            is_active=True,
        )

        get_user_model().objects.create_user(
            email="zaid@example.com",
            name="Zaid Yaseen",
            password="123",
            is_active=True,
        )

        self.stdout.write(self.style.SUCCESS("Successfully created user base."))
