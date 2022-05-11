# Generated by Django 4.0.4 on 2022-05-10 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0007_buylist'),
    ]

    operations = [
        migrations.RenameField(
            model_name='buylist',
            old_name='chapter_id',
            new_name='chapter',
        ),
        migrations.RenameField(
            model_name='buylist',
            old_name='user_id',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='chapter',
            old_name='comic_id',
            new_name='comic',
        ),
        migrations.RenameField(
            model_name='chapterimage',
            old_name='chapter_id',
            new_name='chapter',
        ),
        migrations.RenameField(
            model_name='comic',
            old_name='creator_id',
            new_name='creator',
        ),
        migrations.RenameField(
            model_name='readhistory',
            old_name='chapter_id',
            new_name='chapter',
        ),
        migrations.RenameField(
            model_name='readhistory',
            old_name='user_id',
            new_name='user',
        ),
    ]