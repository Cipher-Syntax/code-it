from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment, Notifications
from posts.models import Posts

@receiver(post_save, sender=Comment)
def notify_user(sender, instance, created, **kwargs):
    if created:
        post = instance.posts
        post_owner = post.user
        commenter = instance.user

        # No notification for self-comments
        if post_owner != commenter:
            Notifications.objects.create(
                user=post_owner, 
                from_user=commenter, 
                posts=post, 
                message=f"{commenter.firstname} commented on your post: '{post.title[:20]}...'",
                is_read=False
        )
