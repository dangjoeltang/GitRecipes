# Generated by Django 2.2.1 on 2019-06-02 22:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0003_auto_20190602_1720'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecipeIngredients',
            new_name='RecipeIngredient',
        ),
    ]