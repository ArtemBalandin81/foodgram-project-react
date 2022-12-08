# Generated by Django 3.2.16 on 2022-12-03 17:27

import colorfield.fields
from django.db import migrations
import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0003_alter_tag_color'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=colorfield.fields.ColorField(default='#FFFFE0', image_field=None, max_length=7, samples=None, validators=[recipes.validators.validate_color], verbose_name='Цвет в HEX'),
        ),
    ]