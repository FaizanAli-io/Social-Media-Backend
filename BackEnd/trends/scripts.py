from .models import Hashtag


def add_hashtags(post):
    hashtag_count = {}

    for word in post.split():
        if word[0] == "#":
            hashtag = word[1:]
            if hashtag in hashtag_count:
                hashtag_count[hashtag] += 1
            else:
                hashtag_count[hashtag] = 1

    print(hashtag_count)

    for key, val in hashtag_count.items():
        hashtags = Hashtag.objects.filter(content=key)
        if hashtags.exists():
            hashtag = hashtags.first()
            hashtag.occurrence += val
        else:
            hashtag = Hashtag.objects.create(
                content=key,
                occurrence=val,
            )
        hashtag.save()
