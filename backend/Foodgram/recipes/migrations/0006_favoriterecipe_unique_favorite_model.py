# Generated by Django 3.2.16 on 2022-12-21 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0005_remove_favoriterecipe_unique_favorite_model'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='favoriterecipe',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_favorite_model'),
        ),
    ]
