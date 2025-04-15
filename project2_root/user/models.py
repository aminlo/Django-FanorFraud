from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    bio = models.TextField(blank=True, null=True, default="No bio yet.")
    profile_picture = models.ImageField(default = 'profile_pics/placeholderuser.jpg', upload_to='profile_pics/', blank=False, null=True)

    def __str__(self):
        return self.username