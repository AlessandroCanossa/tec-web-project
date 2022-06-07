# Generated by Django 4.0.4 on 2022-05-10 14:52

from django.db import migrations, models
import dynamic_image.fields


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0005_readhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chapter',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='chapterimage',
            name='image',
            field=dynamic_image.fields.DynamicImageField(max_length=255, upload_to='dummy'),
        ),
    ]