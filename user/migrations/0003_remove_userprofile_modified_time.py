# Generated by Django 2.2.2 on 2019-07-16 01:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20190715_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='modified_time',
        ),
    ]
