# Generated by Django 2.2.2 on 2019-08-05 23:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0019_auto_20190726_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipephoto',
            name='photo_file',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
