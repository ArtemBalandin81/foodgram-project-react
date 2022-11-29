from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

User = get_user_model()


class Tag(models.Model):
    """Модель тега"""
    name = models.CharField(
        blank=False, max_length=200, verbose_name='Название'
    )
    color = models.CharField(
        blank=False, max_length=7, verbose_name='Цвет в HEX'
    )
    slug = models.SlugField(
        blank=False,
        max_length=200,
        unique=True,
        verbose_name='Уникальный слаг'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'color', 'slug'],
                name='unique_tag'
            ),
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Модель рецепта"""
    author = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор публикации',
    )
    name = models.CharField(
        blank=False, max_length=200, verbose_name='Название'
    )
    # image = models.ImageField(
    #    verbose_name="Картинка", upload_to='posts/', blank=False)
    text = models.TextField(blank=False, verbose_name='Текст поста')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата публикации'
    )
    # ingredients =
    tags = models.ManyToManyField(
        Tag,
        blank=False,
        through='TagReciepe',
        verbose_name='Список тегов',
    )
    cooking_time = models.IntegerField(
        validators=[MinValueValidator(1)], verbose_name='Время приготовления'
    )

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)

    def __str__(self) -> str:
        return self.text[:15]


class TagReciepe(models.Model):
    """Модель для связи id Tag и id Reciepe."""
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    reciepe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.tag} {self.reciepe}'
