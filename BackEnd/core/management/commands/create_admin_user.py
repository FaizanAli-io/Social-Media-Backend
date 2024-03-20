from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):

    def handle(self, *args, **options):

        get_user_model().objects.create_superuser(
            email="admin@example.com",
            name="The Admin",
            password="123",
        )

        self.stdout.write(self.style.SUCCESS("Successfully created admin user."))
