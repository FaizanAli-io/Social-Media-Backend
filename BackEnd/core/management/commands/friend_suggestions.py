from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def handle(self, *args, **options):
        user_model = get_user_model()

        for user in user_model.objects.all():
            user.people_you_may_know.clear()
            my_friends = user.friends.all()

            for friend in my_friends:
                for friend_of_friend in friend.friends.all():
                    if (friend_of_friend not in my_friends) and (
                        friend_of_friend != user
                    ):

                        user.people_you_may_know.add(friend_of_friend)

        self.stdout.write(self.style.SUCCESS("Successfully added people you may know."))
