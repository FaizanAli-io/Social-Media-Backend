from django.core.management.base import BaseCommand

from account.models import User, FriendRequest


class Command(BaseCommand):

    def handle(self, *args, **options):

        for user in User.objects.all():

            user.friends.clear()

        for request in FriendRequest.objects.all():

            request.delete()
