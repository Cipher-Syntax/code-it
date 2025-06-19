from django.db import models
from posts.models import Posts
from users.models import UserRegistration
from datetime import datetime

# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    comments = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='comment_images', blank=True, null=True)
    gif = models.ImageField(upload_to='comment_images', blank=True, null=True)
    liked_by = models.ManyToManyField(UserRegistration, related_name='liked_comments', blank=True)
    reply = models.IntegerField(default=0)
    created_at = models.DateTimeField(default=datetime.now)

    def total_likes(self):
        return self.liked_by.count()


class Notifications(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='notifications')
    from_user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE, related_name='sent_notifications')
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE, blank=True, null=True)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=datetime.now)

    def __str__(self):
        return f'Notifications for {self.user.firstname}'


