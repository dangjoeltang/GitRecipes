# Generated by Django 2.2.1 on 2019-06-02 23:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_auto_20190602_1750'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_text', models.CharField(max_length=24, verbose_name='Tag')),
                ('created_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('modified_time', models.DateTimeField(auto_now=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.Recipe', verbose_name='Recipe tagged')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.Tag', verbose_name='Tag used')),
            ],
        ),
        migrations.AddField(
            model_name='recipe',
            name='tags',
            field=models.ManyToManyField(through='recipe.RecipeTag', to='recipe.Tag'),
        ),
    ]