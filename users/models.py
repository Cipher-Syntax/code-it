from django.db import models


# Create your models here.
class UserRegistration(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.firstname


class Profile(models.Model):
    user = models.ForeignKey(UserRegistration, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    user_profile = models.ImageField(upload_to='profile_images', default='blank_profile.png')
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.firstname
