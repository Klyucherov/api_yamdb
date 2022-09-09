from django.db import models


class Category(models.Model):
    name = models.CharField(verbose_name='Название категории', max_length=250)
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True, max_length=50
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField(verbose_name='Название жанра', max_length=250)
    slug = models.SlugField(
        verbose_name='Идентификатор', unique=True, max_length=50
    )

    class Meta:
        ordering = ('slug',)
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField(
        verbose_name='Название произведения', max_length=250)
    category = models.ForeignKey(
        Category, verbose_name='Категория', related_name='titles',
        on_delete=models.SET_NULL, null=True, db_index=True
    )
    description = models.TextField(
        'Описание произведения', null=True, blank=True
    )
    genre = models.ManyToManyField(
        Genre, verbose_name='Жанр', db_index=True
    )
    rating = models.IntegerField(
        verbose_name='Рейтинг', null=True, default=None, db_index=True
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name
