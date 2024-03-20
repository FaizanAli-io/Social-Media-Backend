from core.models import Post, Notification, FriendRequest


def create_notification(
    request,
    notif_type,
    post_id=None,
    friend_request_id=None,
):
    created_for = None

    if notif_type == "postlike":
        body = f"{request.user.name} liked one of your posts!"
        post = Post.objects.get(id=post_id)
        created_for = post.created_by

    if notif_type == "postcomment":
        body = f"{request.user.name} commented on one of your posts!"
        post = Post.objects.get(id=post_id)
        created_for = post.created_by

    if notif_type == "sentrequest":
        body = f"{request.user.name} sent you a friend request!"
        friend_request = FriendRequest.objects.get(id=friend_request_id)
        created_for = friend_request.created_for

    if notif_type == "acceptedrequest":
        body = f"{request.user.name} accepted your friend request!"
        friend_request = FriendRequest.objects.get(id=friend_request_id)
        created_for = friend_request.created_for

    if notif_type == "rejectedrequest":
        body = f"{request.user.name} rejected your friend request!"
        friend_request = FriendRequest.objects.get(id=friend_request_id)
        created_for = friend_request.created_for

    notification = Notification.objects.create(
        body=body,
        post_id=post_id,
        created_by=request.user,
        created_for=created_for,
        notification_type=notif_type,
    )

    return notification
