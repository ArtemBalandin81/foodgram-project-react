# Generated by Django 3.2.16 on 2022-12-10 10:47

import colorfield.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import recipes.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Ингредиенты')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единицы измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField(validators=[django.core.validators.MinValueValidator(0)], verbose_name='Количество ингредиента')),
            ],
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('image', models.ImageField(default=None, null=True, upload_to='recipes/images/', verbose_name='Фото')),
                ('text', models.TextField(verbose_name='Текст поста')),
                ('pub_date', models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1)], verbose_name='Время приготовления')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ('-pub_date',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название')),
                ('color', colorfield.fields.ColorField(default='#FFFFE0', image_field=None, max_length=7, samples=None, validators=[recipes.validators.validate_color], verbose_name='Цвет в HEX')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Уникальный слаг')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='TagRecipe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tag', to='recipes.recipe')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tag_recipe', to='recipes.tag')),
            ],
        ),
        migrations.AddConstraint(
            model_name='tag',
            constraint=models.UniqueConstraint(fields=('name', 'color', 'slug'), name='unique_tag'),
        ),
    ]
