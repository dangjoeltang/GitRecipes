# Generated by Django 2.2.2 on 2019-07-19 03:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0016_auto_20190716_2052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='privacy',
            field=models.CharField(choices=[('Public', 'Public'), ('Private', 'Private'), ('Secret', 'Secret')], default='public', max_length=10),
        ),
    ]
