# Generated by Django 3.2.6 on 2021-08-07 20:02

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipe', '0002_auto_20210807_0013'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rating',
            old_name='recipe_id',
            new_name='recipe',
        ),
        migrations.AlterField(
            model_name='rating',
            name='value',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.CreateModel(
            name='Meal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('recipes', models.ManyToManyField(to='recipe.Recipe')),
            ],
        ),
    ]
