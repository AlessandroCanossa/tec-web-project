# Generated by Django 4.0.4 on 2022-05-10 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0008_rename_chapter_id_buylist_chapter_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='chapter',
            name='cost',
            field=models.PositiveIntegerField(default=50),
        ),
    ]
