from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal


# Create your models here.


class Room(models.Model):
    class RoomType(models.TextChoices):
        STANDARD = 'standard', 'Стандартное место'
        VIP = 'vip', 'VIP-кабинка'
        MEETING = 'meeting', 'Переговорная'

    title = models.CharField(max_length=100, verbose_name='Название')
    room_type = models.CharField(
        max_length=20,
        choices=RoomType.choices,
        default=RoomType.STANDARD,
        verbose_name='Тип помещения'
    )
    capacity = models.PositiveIntegerField(verbose_name='Вместимость')
    description = models.TextField(blank=True, verbose_name='Описание')

    def __str__(self):
        return f"{self.title} ({self.get_room_type_display()})"

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class Tariff(models.Model):
    class TariffType(models.TextChoices):
        HOURLY = 'hourly', 'Почасовой'
        DAILY = 'daily', 'Дневной'
        WEEKLY = 'weekly', 'Недельный'
        MONTHLY = 'monthly', 'Месячный'

    title = models.CharField(max_length=100, verbose_name='Название тарифа')
    tariff_type = models.CharField(
        max_length=20,
        choices=TariffType.choices,
        verbose_name='Тип тарифа'
    )
    price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))],
        verbose_name='Цена'
    )
    description = models.TextField(blank=True, verbose_name='Описание')
    available_for_vip = models.BooleanField(default=True, verbose_name='Доступен для VIP')

    def __str__(self):
        return f"{self.title} — {self.price} ₽"

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'


class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Помещение')
    tariff = models.ForeignKey(Tariff, on_delete=models.CASCADE, verbose_name='Тариф')
    customer_name = models.CharField(max_length=255, verbose_name='Клиент')
    start_time = models.DateTimeField(verbose_name='Начало брони')
    end_time = models.DateTimeField(verbose_name='Окончание брони')

    def __str__(self):
        return f"Бронь {self.customer_name} — {self.room} ({self.start_time:%d.%m.%Y %H:%M})"

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
