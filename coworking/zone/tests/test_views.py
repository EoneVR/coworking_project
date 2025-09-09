import pytest
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
from zone.models import Room, Tariff, Subscription, UserSubscription, Booking


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    return User.objects.create_user(username="user1", password="123")


@pytest.fixture
def staff_user(db):
    return User.objects.create_user(username="admin", password="1234", is_staff=True)


@pytest.mark.django_db
def test_room_crud(api_client, staff_user):
    api_client.force_authenticate(user=staff_user)

    # create
    resp = api_client.post("/zone/rooms/", {
        "title": "Комната",
        "room_type": Room.RoomType.STANDARD,
        "capacity": 3,
        "description": "Тест"
    }, format="json")
    assert resp.status_code == 201
    room_id = resp.data["id"]

    # list
    resp = api_client.get("/zone/rooms/")
    assert resp.status_code == 200
    assert len(resp.data) == 4

    # retrieve
    resp = api_client.get(f"/zone/rooms/{room_id}/")
    assert resp.status_code == 200
    assert resp.data["title"] == "Комната"

    # update
    resp = api_client.patch(f"/zone/rooms/{room_id}/", {"capacity": 5}, format="json")
    assert resp.status_code == 200
    assert resp.data["capacity"] == 5

    # delete
    resp = api_client.delete(f"/zone/rooms/{room_id}/")
    assert resp.status_code == 204


@pytest.mark.django_db
def test_user_subscription_queryset(api_client, user, staff_user):
    sub = Subscription.objects.create(title="Месяц", duration="month", price=Decimal("1000.00"))
    user_sub = UserSubscription.objects.create(
        user=user,
        subscription=sub,
        start_date=timezone.now().date(),
        end_date=timezone.now().date() + timedelta(days=30)
    )

    api_client.force_authenticate(user=user)
    resp = api_client.get("/zone/user-subscriptions/")
    assert len(resp.data) == 4
    assert resp.data["results"][0]["id"] == user_sub.id

    api_client.force_authenticate(user=staff_user)
    resp = api_client.get("/zone/user-subscriptions/")
    assert any(r["id"] == user_sub.id for r in resp.data["results"])


@pytest.mark.django_db
def test_booking_creation_and_task_mock(api_client, user, mocker):
    room = Room.objects.create(title="VIP", room_type=Room.RoomType.VIP, capacity=2)
    Tariff.objects.create(title="VIP тариф", price_per_hour=Decimal("200.00"), room_type=Room.RoomType.VIP)

    start_time = timezone.now() + timedelta(hours=1)
    end_time = start_time + timedelta(hours=2)

    mocked_task = mocker.patch("zone.views.send_booking_confirmation.delay")

    api_client.force_authenticate(user=user)
    resp = api_client.post("/zone/bookings/", {
        "room": room.id,
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat()
    }, format="json")

    assert resp.status_code == 201
    booking_id = resp.data["id"]
    booking = Booking.objects.get(id=booking_id)

    mocked_task.assert_called_once_with(booking.id)

    assert booking.price == Decimal("400.00")


@pytest.mark.django_db
def test_booking_queryset_restriction(api_client, user, staff_user):
    room = Room.objects.create(title="Комната", room_type=Room.RoomType.STANDARD, capacity=3)
    Tariff.objects.create(title="Стандарт", price_per_hour=Decimal("100.00"), room_type=Room.RoomType.STANDARD)

    booking = Booking.objects.create(
        user=user,
        room=room,
        start_time=timezone.now() + timedelta(hours=1),
        end_time=timezone.now() + timedelta(hours=2),
        price=Decimal("100.00")
    )

    api_client.force_authenticate(user=user)
    resp = api_client.get("/zone/bookings/")
    assert any(b["id"] == booking.id for b in resp.data["results"])

    other = User.objects.create_user(username="other", password="123")
    api_client.force_authenticate(user=other)
    resp = api_client.get("/zone/bookings/")
    assert all(b["id"] != booking.id for b in resp.data["results"])

    api_client.force_authenticate(user=staff_user)
    resp = api_client.get("/zone/bookings/")
    assert any(b["id"] == booking.id for b in resp.data["results"])
