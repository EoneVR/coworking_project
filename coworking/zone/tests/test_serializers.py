import pytest
from django.utils import timezone
from django.contrib.auth.models import User
from datetime import timedelta
from decimal import Decimal

from zone.models import Room, Tariff, Subscription, UserSubscription, Booking
from zone.serializers import (
    RoomSerializer, TariffSerializer, SubscriptionSerializer,
    UserSubscriptionSerializer, BookingSerializer
)


@pytest.mark.django_db
def test_room_serializer():
    room = Room.objects.create(
        title="Комната №1",
        room_type=Room.RoomType.STANDARD,
        capacity=5,
        description="Тестовая комната"
    )
    data = RoomSerializer(room).data
    assert data["title"] == "Комната №1"
    assert data["capacity"] == 5


@pytest.mark.django_db
def test_tariff_serializer():
    tariff = Tariff.objects.create(
        title="Базовый",
        price_per_hour=Decimal("100.50"),
        room_type=Room.RoomType.VIP,
    )
    data = TariffSerializer(tariff).data
    assert data["price_per_hour"] == 100.50
    assert data["room_type"] == Room.RoomType.VIP


@pytest.mark.django_db
def test_subscription_serializer():
    sub = Subscription.objects.create(
        title="Месячная подписка",
        duration=Subscription.Duration.MONTH,
        price=Decimal("1500.00")
    )
    data = SubscriptionSerializer(sub).data
    assert data["title"] == "Месячная подписка"
    assert data["duration"] == Subscription.Duration.MONTH


@pytest.mark.django_db
def test_user_subscription_serializer_create_new_subscription():
    user = User.objects.create_user(username="testuser", password="123")
    sub = Subscription.objects.create(
        title="Неделя",
        duration=Subscription.Duration.WEEK,
        price=Decimal("300.00")
    )

    serializer = UserSubscriptionSerializer(
        data={"subscription": sub.id},
        context={"request": type("Request", (), {"user": user})()}
    )
    assert serializer.is_valid(), serializer.errors
    user_sub = serializer.save()

    assert user_sub.user == user
    assert user_sub.subscription == sub
    assert user_sub.is_active


@pytest.mark.django_db
def test_user_subscription_serializer_prolong_existing():
    user = User.objects.create_user(username="prolong_user", password="123")
    sub = Subscription.objects.create(
        title="Месяц",
        duration=Subscription.Duration.MONTH,
        price=Decimal("1000.00")
    )
    active = UserSubscription.objects.create(
        user=user,
        subscription=sub,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=30)
    )

    serializer = UserSubscriptionSerializer(
        data={"subscription": sub.id},
        context={"request": type("Request", (), {"user": user})()}
    )
    assert serializer.is_valid()
    updated = serializer.save()

    assert updated.id == active.id
    assert updated.end_date > active.start_date


@pytest.mark.django_db
def test_booking_serializer_valid():
    user = User.objects.create_user(username="booker", password="123")
    room = Room.objects.create(
        title="VIP кабинет",
        room_type=Room.RoomType.VIP,
        capacity=2
    )
    Tariff.objects.create(
        title="VIP тариф",
        price_per_hour=Decimal("200.00"),
        room_type=Room.RoomType.VIP
    )

    start_time = timezone.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)

    serializer = BookingSerializer(
        data={"room": room.id, "start_time": start_time, "end_time": end_time},
        context={"request": type("Request", (), {"user": user})()}
    )
    assert serializer.is_valid(), serializer.errors
    booking = serializer.save()

    assert booking.user == user
    assert booking.room == room
    assert booking.price == Decimal("400.00")


@pytest.mark.django_db
def test_booking_serializer_invalid_overlap():
    user = User.objects.create_user(username="booker2", password="123")
    room = Room.objects.create(
        title="Комната",
        room_type=Room.RoomType.STANDARD,
        capacity=3
    )
    Tariff.objects.create(
        title="Стандарт",
        price_per_hour=Decimal("100.00"),
        room_type=Room.RoomType.STANDARD
    )

    start_time = timezone.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)

    Booking.objects.create(
        user=user,
        room=room,
        start_time=start_time,
        end_time=end_time,
        price=Decimal("200.00")
    )

    serializer = BookingSerializer(
        data={"room": room.id, "start_time": start_time, "end_time": end_time},
        context={"request": type("Request", (), {"user": user})()}
    )
    assert not serializer.is_valid()
    assert "Комната уже занята" in str(serializer.errors)
