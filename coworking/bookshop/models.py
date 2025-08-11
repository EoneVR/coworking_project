from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

# Create your models here.


class Book(models.Model):
    class Binding(models.TextChoices):
        HARD = 'hard', 'Твёрдый переплёт'
        SOFT = 'soft', 'Мягкий переплёт'

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(default='Описание', verbose_name='Описание')
    author = models.CharField(max_length=255, verbose_name='Автор')
    year_of_publish = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1000),
            MaxValueValidator(date.today().year)
        ],
        verbose_name='Год публикации'
    )
    pages = models.PositiveIntegerField(default=0, verbose_name='Кол-во страниц')
    binding = models.CharField(
        max_length=10,
        choices=Binding.choices,
        default=Binding.HARD,
        verbose_name='Переплёт'
    )
    in_stock = models.PositiveIntegerField(default=0, verbose_name='Кол-во в магазине')

    def __str__(self):
        return f"{self.title} — {self.author}"

    class Meta:
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

