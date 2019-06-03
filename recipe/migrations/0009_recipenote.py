# Generated by Django 2.2.1 on 2019-06-03 00:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0008_auto_20190602_1846'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecipeNote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note_text', models.TextField(verbose_name='Note')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.Recipe')),
            ],
            options={
                'verbose_name': 'Extra Note about Recipe',
                'verbose_name_plural': 'Extra Notes about Recipe',
            },
        ),
    ]
