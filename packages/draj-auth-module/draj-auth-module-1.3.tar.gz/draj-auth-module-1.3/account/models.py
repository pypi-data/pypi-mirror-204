from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    username = models.CharField("Username", max_length=100)
    first_name = models.CharField("First Name", max_length=64)
    last_name = models.CharField("Last Name", max_length=64)
    email = models.CharField("Email", max_length=80, unique=True)
    password = models.CharField("Password", max_length=100)
    is_active = models.BooleanField("Is Active", default=False)

    def __str__(self):
        return str(self.username)
