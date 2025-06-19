from django.db import models
from users.models import UserRegistration
from datetime import datetime
import uuid

# Create your models here.
class Posts(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    title = models.TextField()
    image = models.ImageField(upload_to='post_images', blank=True, null=True)
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=datetime.now)
    likes = models.ManyToManyField(UserRegistration, related_name='liked_posts', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return f"{self.user.firstname}'s Post"
