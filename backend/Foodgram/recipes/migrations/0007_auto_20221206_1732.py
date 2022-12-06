# Generated by Django 3.2.16 on 2022-12-06 12:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_alter_ingredientrecipe_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredientrecipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='tagrecipe',
            name='tags',
        ),
        migrations.AddField(
            model_name='ingredientrecipe',
            name='ingredient',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='ingredient_recipe', to='recipes.ingredient'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tagrecipe',
            name='tag',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='tag_recipe', to='recipes.tag'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='ingredientrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredient', to='recipes.recipe'),
        ),
        migrations.AlterField(
            model_name='tagrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_tag', to='recipes.recipe'),
        ),
    ]
