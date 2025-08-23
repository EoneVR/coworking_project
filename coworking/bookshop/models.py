from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from datetime import date
from decimal import Decimal
from uuid import uuid4


# Create your models here.

class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название категории')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Book(models.Model):
    class Binding(models.TextChoices):
        HARD = 'hard', 'Твёрдый переплёт'
        SOFT = 'soft', 'Мягкий переплёт'

    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(default='Описание', verbose_name='Описание')
    author = models.CharField(max_length=255, verbose_name='Автор')
    unit_price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=1,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name='Цена за 1 ед.'
    )
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
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return f"{self.title} — {self.author}"

    class Meta:
        ordering = ['title']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Корзина {self.id} от {self.created_at:%Y-%m-%d}"

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина', related_name='items')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, verbose_name='Книга')
    quantity = models.PositiveIntegerField(verbose_name='Кол-во книг')

    class Meta:
        verbose_name = 'Книга в корзине'
        verbose_name_plural = 'Книги в корзинах'


class Order(models.Model):
    class PaymentStatus(models.TextChoices):
        PENDING = 'P', 'Pending'
        COMPLETE = 'C', 'Complete'
        FAILED = 'F', 'Failed'

    customer = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='Покупатель')
    placed_at = models.DateTimeField(auto_now_add=True, verbose_name='Время заказа')
    payment_status = models.CharField(
        max_length=1,
        choices=PaymentStatus.choices,
        default=PaymentStatus.PENDING,
        verbose_name='Статус оплаты'
    )

    def __str__(self):
        return f"Заказ {self.id} — {self.get_payment_status_display()}"

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='Заказ',
                              related_name='items')
    book = models.ForeignKey(Book, on_delete=models.PROTECT, verbose_name='Книга')
    quantity = models.PositiveIntegerField(verbose_name='Количество книг')
    unit_price = models.DecimalField(max_digits=6, decimal_places=2,
                                     verbose_name='Цена за книгу')

    class Meta:
        verbose_name = 'Книга в заказе'
        verbose_name_plural = 'Книги в заказах'
