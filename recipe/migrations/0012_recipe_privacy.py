# Generated by Django 2.2.2 on 2019-07-16 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0011_auto_20190715_2105'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='privacy',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Public'), ('secret', 'Secret')], default='public', max_length=10),
        ),
    ]
