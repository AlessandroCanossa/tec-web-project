import time

from django.db import models
from django.contrib.auth import models as auth_models
from dynamic_image.fields import DynamicImageField

from . import managers


# Create your models here.


class User(auth_models.AbstractUser):
    coins = models.IntegerField(default=0)
    is_creator = models.BooleanField(default=False)

    email = models.EmailField(max_length=255, unique=True)

    objects = managers.UserManager()

    def __str__(self):
        return self.username


class Genre(models.Model):
    name = models.CharField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Comic(models.Model):
    ONGOING = 'O'
    HIATUS = 'H'
    COMPLETED = 'C'
    CANCELLED = 'D'
    STATUS = [
        (ONGOING, 'ONGOING'),
        (HIATUS, 'HIATUS'),
        (COMPLETED, 'COMPLETED'),
        (CANCELLED, 'CANCELLED'),
    ]

    title = models.CharField(unique=True, max_length=255)
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    genres = models.ManyToManyField(to=Genre)
    watches = models.PositiveBigIntegerField(default=0)
    follows = models.PositiveBigIntegerField(default=0)
    rating = models.FloatField(default=0)
    status = models.CharField(choices=STATUS, default=ONGOING, max_length=1)
    summary = models.TextField()
    thumbnail = DynamicImageField()
    cover = DynamicImageField()

    def __str__(self):
        return self.title

    def get_upload_to(self, field_name):
        class_name = self.__class__.__name__.lower()
        instance_name = self.title.lower().replace(' ', '-')
        return f'{class_name}/{instance_name}'


class Chapter(models.Model):
    title = models.CharField(max_length=255)
    comic = models.ForeignKey(to=Comic, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveBigIntegerField(default=0)

    models.UniqueConstraint(fields=['title', 'comic'], name='comic_chapter')

    def __str__(self):
        return f'{self.comic.title} - {self.title}'


class ChapterImage(models.Model):
    image = DynamicImageField()
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)

    models.UniqueConstraint(fields=['image', 'chapter'], name='chapter_image')

    def __str__(self):
        return self.image.name

    def get_upload_to(self, field_name):
        chapter_name = self.chapter.title.lower().replace(' ', '-')
        comic_name = self.chapter.comic.title.lower().replace(' ', '-')
        return f'chapter/{comic_name}/{chapter_name}'


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
