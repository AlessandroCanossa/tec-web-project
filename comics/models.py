from django.db import models
from dynamic_image.fields import DynamicImageField

from users.models import User


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
    genre = models.ManyToManyField(to=Genre)
    watches = models.PositiveBigIntegerField(default=0)
    follows = models.PositiveBigIntegerField(default=0)
    rating = models.FloatField(default=0)
    status = models.CharField(choices=STATUS, default=ONGOING, max_length=1)
    summary = models.TextField()
    cover = DynamicImageField()

    def __str__(self):
        return self.title

    def get_upload_to(self, field_name):
        class_name = self.__class__.__name__.lower()
        instance_name = self.title.lower().replace(' ', '-')
        return f'{class_name}/{instance_name}'

    def delete(self, using=None, keep_parents=False):
        self.cover.delete()
        super().delete(using, keep_parents)


class Chapter(models.Model):
    chapter_num = models.PositiveIntegerField()
    comic = models.ForeignKey(to=Comic, on_delete=models.CASCADE)
    pub_date = models.DateTimeField(auto_now_add=True)
    likes = models.PositiveBigIntegerField(default=0)
    cost = models.PositiveIntegerField(default=50)

    models.UniqueConstraint(fields=['chapter_num', 'comic'], name='comic_chapter')

    def __str__(self):
        return f'{self.comic.title} - chapter-{self.chapter_num}'


class ChapterImage(models.Model):
    image = DynamicImageField()
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)

    models.UniqueConstraint(fields=['image', 'chapter'], name='chapter_image')

    def __str__(self):
        return self.image.name

    def get_upload_to(self, field_name):
        chapter_name = self.chapter.chapter_num
        comic_name = self.chapter.comic.title.lower().replace(' ', '-')
        return f'chapter/{comic_name}/chapter-{chapter_name}'

    def delete(self, using=None, keep_parents=False):
        self.image.delete()
        super().delete(using, keep_parents)


class Rating(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comic = models.ForeignKey(to=Comic, on_delete=models.CASCADE, related_name='user_rating')
    rating = models.PositiveIntegerField()

    models.UniqueConstraint(fields=['user', 'comic'], name='unique_rating')

    def __str__(self):
        return f'{self.user.username} - {self.comic.title} - {self.rating}'


class Like(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    chapter = models.ForeignKey(to=Chapter, on_delete=models.CASCADE)

    models.UniqueConstraint(fields=['user', 'chapter'], name='unique_like')

    def __str__(self):
        return f'{self.user.username} - {self.chapter.comic.title} - {self.chapter.chapter_num}'


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


class Library(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    comic = models.ForeignKey(to=Comic, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.comic.title}'
