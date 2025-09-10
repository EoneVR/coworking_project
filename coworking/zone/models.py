from django.db import models
from django.core.validators import MinValueValidator
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

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
    image = models.ImageField(
        upload_to='room_images/',
        null=True, blank=True,
        verbose_name='Фото'
    )
    def __str__(self):
        return f"{self.title} ({self.get_room_type_display()})"

    def is_available(self, start_time, end_time, exclude_booking_id=None):
        qs = Booking.objects.filter(
            room=self,
            start_time__lt=end_time,
            end_time__gt=start_time
        )
        if exclude_booking_id:
            qs = qs.exclude(id=exclude_booking_id)
        return not qs.exists()

    class Meta:
        verbose_name = 'Помещение'
        verbose_name_plural = 'Помещения'


class Tariff(models.Model):
    title = models.CharField(max_length=100)
    price_per_hour = models.DecimalField(
        max_digits=8, decimal_places=2,
        validators=[MinValueValidator(Decimal("0.01"))]
    )
    room_type = models.CharField(max_length=20, choices=Room.RoomType.choices)

    def __str__(self):
        return f"{self.title} ({self.room_type})"

    class Meta:
        verbose_name = 'Тариф'
        verbose_name_plural = 'Тарифы'


class Subscription(models.Model):
    class Duration(models.TextChoices):
        WEEK = "week", "1 неделя"
        MONTH = "month", "1 месяц"
        THREE_MONTHS = "3_months", "3 месяца"
        SIX_MONTHS = "6_months", "6 месяцев"

    title = models.CharField(max_length=100)
    duration = models.CharField(max_length=20, choices=Duration.choices)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(
        upload_to='subscription_images/',
        null=True, blank=True,
        verbose_name='Фото'
    )
    def get_end_date(self, start_date):
        if self.duration == self.Duration.WEEK:
            return start_date + timedelta(weeks=1)
        elif self.duration == self.Duration.MONTH:
            return start_date + timedelta(days=30)
        elif self.duration == self.Duration.THREE_MONTHS:
            return start_date + timedelta(days=90)
        elif self.duration == self.Duration.SIX_MONTHS:
            return start_date + timedelta(days=180)
        return start_date

    def __str__(self):
        return f"{self.title} ({self.get_duration_display()})"

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class UserSubscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE)
    start_date = models.DateField(default=now)
    end_date = models.DateField()

    def save(self, *args, **kwargs):
        if not self.end_date:  # если не указана вручную
            self.end_date = self.subscription.get_end_date(self.start_date)
        super().save(*args, **kwargs)

    @property
    def is_active(self):
        return self.start_date <= now().date() <= self.end_date

    def remaining_days(self):
        today = timezone.now().date()
        if self.end_date < today:
            return 0
        return (self.end_date - today).days

    def __str__(self):
        return f"{self.user} — {self.subscription.title} (до {self.end_date})"

    class Meta:
        verbose_name = 'Подписка клиента'
        verbose_name_plural = 'Подписки клиентов'


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name='Помещение')
    start_time = models.DateTimeField(verbose_name='Начало брони')
    end_time = models.DateTimeField(verbose_name='Окончание брони')
    subscription = models.ForeignKey(
        UserSubscription, on_delete=models.SET_NULL, null=True, blank=True
    )
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user} → {self.room} [{self.start_time:%d.%m %H:%M}]"

    MAX_HOURS = 12

    def clean(self):
        now_dt = timezone.now()
        # 1) не разрешаем бронь в прошлом
        if self.start_time < now_dt:
            raise ValidationError("Нельзя создать бронь в прошлом")

        # 2) проверка что конец позже начала
        if self.end_time <= self.start_time:
            raise ValidationError("Окончание брони должно быть позже начала")

        # 3) ограничение по длительности
        duration_hours = (self.end_time - self.start_time).total_seconds() / 3600
        if duration_hours > self.MAX_HOURS:
            raise ValidationError(f"Максимальная длительность брони — {self.MAX_HOURS} часов")

        # 4) проверка пересечений бронирований
        overlaps = Booking.objects.filter(
            room=self.room,
            start_time__lt=self.end_time,
            end_time__gt=self.start_time
        ).exclude(id=self.id)
        if overlaps.exists():
            raise ValidationError("Это время уже забронировано")

        # 5) если привязана подписка — она должна принадлежать пользователю и быть активной
        if self.subscription:
            if self.subscription.user != self.user:
                raise ValidationError("Подписка не принадлежит этому пользователю")
            if not self.subscription.is_active:
                raise ValidationError("Привязанная подписка не активна")

    def calculate_price(self):
        duration_hours = (self.end_time - self.start_time).total_seconds() / 3600
        duration_hours = Decimal(duration_hours).quantize(Decimal("0.01"))

        # если есть активная подписка — бесплатно
        if self.subscription and self.subscription.is_active:
            return Decimal("0.00")

        tariff = Tariff.objects.filter(room_type=self.room.room_type).first()
        if not tariff:
            raise ValidationError(f"Не найден тариф для типа комнаты: {self.room.room_type}")

        return (tariff.price_per_hour * duration_hours).quantize(Decimal("0.01"))

    def save(self, *args, **kwargs):
        self.full_clean()
        self.price = self.calculate_price()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Бронирование'
        verbose_name_plural = 'Бронирования'
