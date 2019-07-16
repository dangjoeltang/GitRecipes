# Generated by Django 2.2.2 on 2019-07-16 01:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='modified_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='profile_photo',
            field=models.FileField(blank=True, upload_to=''),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='short_bio',
            field=models.CharField(blank=True, max_length=400),
        ),
    ]
