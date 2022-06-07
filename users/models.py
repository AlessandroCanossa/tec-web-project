from django.contrib.auth import models as auth_models
from django.db import models

from users import managers


class User(auth_models.AbstractUser):
    coins = models.IntegerField(default=0)
    is_creator = models.BooleanField(default=False)

    email = models.EmailField(max_length=255, unique=True)

    objects = managers.UserManager()

    def __str__(self):
        return self.username


class CoinsPurchase(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    coins = models.PositiveIntegerField()
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} - {self.coins} coins - {self.date}'

