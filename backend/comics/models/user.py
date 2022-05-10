from django.db import models
from django.contrib.auth import models as auth_models

from .. import managers
from .comics import *


class User(auth_models.AbstractUser):
    coins = models.IntegerField(default=0)
    is_creator = models.BooleanField(default=False)

    email = models.EmailField(max_length=255, unique=True)

    objects = managers.UserManager()

    def __str__(self):
        return self.username


class ReadHistory(models.Model):
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} - {self.chapter} - {self.date}'


class BuyList(models.Model):
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    date = models.DateField(auto_now_add=True)

    models.UniqueConstraint(fields=['user', 'chapter'], name='bought_chapter')

    def __str__(self):
        return f'{self.user} - {self.chapter} - {self.date}'


class Comment(models.Model):
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(to='Comment', on_delete=models.CASCADE, blank=True, null=True, related_name='reply_to')

    def __str__(self):
        return f'Comment {self.body} by {self.user.username}'
