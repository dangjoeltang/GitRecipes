# Generated by Django 2.2.1 on 2019-06-02 22:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_auto_20190602_1744'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='ingredient',
            name='modified_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='created_time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='recipe',
            name='modified_time',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]