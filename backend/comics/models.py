from django.db import models
from django.contrib.auth import models as auth_models

from . import managers
# Create your models here.


class User(auth_models.AbstractUser):
    coins = models.IntegerField(default=0)
    is_creator = models.BooleanField(default=False)

    email = models.EmailField(max_length=255, unique=True)

    objects = managers.UserManager()

    def __str__(self):
        return self.username

