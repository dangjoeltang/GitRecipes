# Generated by Django 2.2.2 on 2019-07-16 02:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0010_auto_20190624_1231'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='description',
            field=models.CharField(blank=True, default='No description available.', max_length=400, verbose_name='Recipe Description'),
        ),
        migrations.CreateModel(
            name='RecipePhotos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo_text', models.CharField(blank=True, default='', max_length=200)),
                ('photo_file', models.FileField(blank=True, upload_to='recipes/')),
                ('uploaded_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_photos', to='recipe.Recipe')),
            ],
        ),
    ]
