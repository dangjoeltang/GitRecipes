# Generated by Django 2.2.2 on 2019-07-16 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0013_auto_20190715_2323'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipePhotos',
            new_name='RecipePhoto',
        ),
    ]