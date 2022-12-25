# Generated by Django 3.2.16 on 2022-12-23 04:02

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0006_favoriterecipe_unique_favorite_model'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShoppingCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_shopping_list', to='recipes.recipe', verbose_name='Рецепт для покупки')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopping_recipes', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь-покупатель')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Список покупок',
                'ordering': ['user'],
            },
        ),
        migrations.AddConstraint(
            model_name='shoppingcart',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_shopping_list_model'),
        ),
    ]