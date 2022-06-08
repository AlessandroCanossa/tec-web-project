from django.db import models

# Create your models here.
from users.models import User
from comics.models import Chapter


class Comment(models.Model):
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    reply = models.ForeignKey(
        'self', on_delete=models.CASCADE, blank=True, null=True, related_name='reply_to')

    def __str__(self):
        return f'Comment {self.body} by {self.user.username}'


class CommentLike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} likes {self.comment.body}'


class CommentDislike(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comment = models.ForeignKey(to=Comment, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} dislikes {self.comment.body}'
