from django.utils import timezone

from django.core.management.base import BaseCommand

from core.models import Post, Hashtag


class Command(BaseCommand):
    def handle(self, *args, **options):
        last_week = timezone.now() - timezone.timedelta(7)
        posts = Post.objects.filter(created_at__gte=last_week, body__contains="#")

        hashtag_count = {}
        for post in posts:
            for word in post.body.split():
                if word[0] == "#":
                    hashtag = word[1:]
                    if hashtag in hashtag_count:
                        hashtag_count[hashtag] += 1
                    else:
                        hashtag_count[hashtag] = 1

        for hashtag in Hashtag.objects.all():
            hashtag.delete()

        for key, value in hashtag_count.items():
            hashtag = Hashtag.objects.create(content=key)
            hashtag.occurrence = value
            hashtag.save()

        self.stdout.write(self.style.SUCCESS("Successfully added trends."))
