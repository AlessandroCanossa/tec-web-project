# Generated by Django 4.0.5 on 2022-06-06 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comics', '0016_coinspurchase_delete_market'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comic',
            name='thumbnail',
        ),
    ]