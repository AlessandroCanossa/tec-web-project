from django.db import models

# Create your models here.
from users.models import User
from comics.models import Chapter


class Comment(models.Model):
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, related_name='reply_to')

    def __str__(self):
        return f'Comment {self.body} by {self.user.username}'
