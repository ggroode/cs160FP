# Generated by Django 3.2.6 on 2021-08-06 22:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import recipe.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=250)),
                ('cookingTime', models.IntegerField()),
                ('image', models.ImageField(upload_to='')),
                ('classification', models.CharField(choices=[('de', 'Dessert'), ('en', 'Entree'), ('si', 'Side'), ('ap', 'Appetizer'), ('dr', 'Drink')], default='en', max_length=2)),
                ('servings', models.IntegerField()),
                ('servingSize', models.CharField(max_length=50)),
                ('private', models.BooleanField(default=False)),
                ('ingredients', models.JSONField(default=dict)),
                ('steps', models.JSONField(default=recipe.models.get_list)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('recipe', models.ManyToManyField(to='recipe.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipe_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('name', models.CharField(max_length=15, primary_key=True, serialize=False, unique=True)),
                ('recipe', models.ManyToManyField(to='recipe.Recipe')),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipe.recipe')),
            ],
        ),
    ]
