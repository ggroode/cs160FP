# Generated by Django 3.2.6 on 2021-08-07 00:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='ingredient',
            old_name='recipe',
            new_name='recipes',
        ),
        migrations.RenameField(
            model_name='tag',
            old_name='recipe',
            new_name='recipes',
        ),
    ]