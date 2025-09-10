from decimal import Decimal
from django.core.validators import MinValueValidator
from django.db import models


# Create your models here.


class Promotion(models.Model):
    description = models.CharField(max_length=255, verbose_name='Описание')
    discount = models.FloatField(
        verbose_name='Процент скидки',
        validators=[MinValueValidator(0.0)]
    )

    def __str__(self):
        return f"{self.description} ({self.discount}%)"

    class Meta:
        verbose_name = 'Акция'
        verbose_name_plural = 'Акции'


class Coffee(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    size = models.CharField(max_length=50, verbose_name='Размер')
    ingredients = models.TextField(verbose_name='Ингредиенты')
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name='Цена за 1 ед.'
    )
    slug = models.SlugField(unique=True, allow_unicode=True)
    promotion = models.ManyToManyField(
        Promotion,
        blank=True,
        related_name="coffees"
    )
    image = models.ImageField(
        upload_to='coffee_images/',
        null=True, blank=True,
        verbose_name='Фото'
    )

    def __str__(self):
        return f"{self.title} ({self.size})"

    class Meta:
        ordering = ['title']
        verbose_name = 'Кофе'
        verbose_name_plural = 'Кофе'


class Bakery(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')
    ingredients = models.TextField(verbose_name='Ингредиенты')
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name='Цена за 1 ед.'
    )
    slug = models.SlugField(unique=True, allow_unicode=True)
    promotion = models.ManyToManyField(
        Promotion,
        blank=True,
        related_name="bakeries"
    )
    in_stock = models.PositiveIntegerField(
        default=0,
        verbose_name='Кол-во в магазине'
    )
    image = models.ImageField(
        upload_to='bakery_images/',
        null=True, blank=True,
        verbose_name='Фото'
    )
    def __str__(self):
        return f"{self.title} ({self.in_stock} шт.)"

    class Meta:
        ordering = ['title']
        verbose_name = 'Выпечка'
        verbose_name_plural = 'Выпечка'
