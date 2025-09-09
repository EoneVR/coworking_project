import pytest
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal

from zone.models import Room, Tariff, Subscription, UserSubscription, Booking
from django.contrib.auth.models import User


@pytest.mark.django_db
class TestRoom:
    def test_str_and_is_available(self):
        room = Room.objects.create(title="Комната 1", room_type=Room.RoomType.STANDARD, capacity=5)
        assert str(room) == "Комната 1 (Стандартное место)"
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        assert room.is_available(start, end) is True


@pytest.mark.django_db
class TestTariff:
    def test_str(self):
        tariff = Tariff.objects.create(title="Базовый", price_per_hour=10, room_type=Room.RoomType.STANDARD)
        assert str(tariff) == "Базовый (standard)"


@pytest.mark.django_db
class TestSubscription:
    def test_get_end_date(self):
        sub = Subscription.objects.create(title="Месяц", duration=Subscription.Duration.MONTH, price=100)
        start = timezone.now().date()
        end = sub.get_end_date(start)
        assert (end - start).days == 30

    def test_str(self):
        sub = Subscription.objects.create(title="Неделя", duration=Subscription.Duration.WEEK, price=50)
        assert "Неделя" in str(sub)


@pytest.mark.django_db
class TestUserSubscription:
    def test_save_and_properties(self):
        user = User.objects.create_user("test", password="123")
        sub = Subscription.objects.create(title="Неделя", duration=Subscription.Duration.WEEK, price=50)
        user_sub = UserSubscription.objects.create(user=user, subscription=sub, start_date=timezone.now().date())
        assert user_sub.end_date == sub.get_end_date(user_sub.start_date)
        assert user_sub.is_active is True
        assert user_sub.remaining_days() <= 7
        assert str(user_sub).startswith("test —")

    def test_expired_subscription(self):
        user = User.objects.create_user("test2", password="123")
        sub = Subscription.objects.create(title="Неделя", duration=Subscription.Duration.WEEK, price=50)
        user_sub = UserSubscription.objects.create(
            user=user, subscription=sub,
            start_date=timezone.now().date() - timedelta(days=10),
            end_date=timezone.now().date() - timedelta(days=3)
        )
        assert user_sub.is_active is False
        assert user_sub.remaining_days() == 0


@pytest.mark.django_db
class TestBooking:
    def setup_method(self):
        self.user = User.objects.create_user("booker", password="123")
        self.room = Room.objects.create(title="VIP комната", room_type=Room.RoomType.VIP, capacity=2)
        self.tariff = Tariff.objects.create(title="VIP тариф", price_per_hour=Decimal("20.00"), room_type=self.room.room_type)

    def test_str(self):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        booking = Booking(user=self.user, room=self.room, start_time=start, end_time=end)
        booking.save()
        assert "booker" in str(booking)

    def test_clean_cannot_book_past(self):
        start = timezone.now() - timedelta(hours=1)
        end = start + timedelta(hours=2)
        booking = Booking(user=self.user, room=self.room, start_time=start, end_time=end)
        with pytest.raises(ValidationError, match="Нельзя создать бронь в прошлом"):
            booking.full_clean()

    def test_clean_end_before_start(self):
        start = timezone.now() + timedelta(hours=1)
        end = start - timedelta(minutes=30)
        booking = Booking(user=self.user, room=self.room, start_time=start, end_time=end)
        with pytest.raises(ValidationError, match="Окончание брони должно быть позже начала"):
            booking.full_clean()

    def test_clean_overlap(self):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        Booking.objects.create(user=self.user, room=self.room, start_time=start, end_time=end, price=10)
        overlap = Booking(user=self.user, room=self.room, start_time=start + timedelta(minutes=30), end_time=end + timedelta(hours=1))
        with pytest.raises(ValidationError, match="Это время уже забронировано"):
            overlap.full_clean()

    def test_clean_subscription_checks(self):
        sub = Subscription.objects.create(title="Неделя", duration=Subscription.Duration.WEEK, price=0)
        user_sub = UserSubscription.objects.create(user=self.user, subscription=sub, start_date=timezone.now().date())
        other_user = User.objects.create_user("other", password="123")

        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)

        # чужая подписка
        booking = Booking(user=other_user, room=self.room, start_time=start, end_time=end, subscription=user_sub)
        with pytest.raises(ValidationError, match="Подписка не принадлежит этому пользователю"):
            booking.full_clean()

        # неактивная подписка
        expired = UserSubscription.objects.create(
            user=self.user, subscription=sub,
            start_date=timezone.now().date() - timedelta(days=10),
            end_date=timezone.now().date() - timedelta(days=3)
        )
        booking = Booking(user=self.user, room=self.room, start_time=start, end_time=end, subscription=expired)
        with pytest.raises(ValidationError, match="Привязанная подписка не активна"):
            booking.full_clean()

    def test_calculate_price_with_tariff(self):
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        booking = Booking(user=self.user, room=self.room, start_time=start, end_time=end)
        booking.save()
        assert booking.price == Decimal("40.00")  # 2 часа * 20

    def test_calculate_price_with_subscription(self):
        sub = Subscription.objects.create(title="Неделя", duration=Subscription.Duration.WEEK, price=0)
        user_sub = UserSubscription.objects.create(user=self.user, subscription=sub, start_date=timezone.now().date())
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        booking = Booking(user=self.user, room=self.room, start_time=start, end_time=end, subscription=user_sub)
        booking.save()
        assert booking.price == Decimal("0.00")

    def test_calculate_price_no_tariff(self):
        # удалим тариф для комнаты
        Tariff.objects.all().delete()
        start = timezone.now() + timedelta(hours=1)
        end = start + timedelta(hours=2)
        booking = Booking(user=self.user, room=self.room, start_time=start, end_time=end)
        with pytest.raises(ValidationError, match="Не найден тариф"):
            booking.full_clean()
            booking.calculate_price()
