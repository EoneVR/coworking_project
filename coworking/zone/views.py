from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.cache import cache
from .models import *
from .serializers import RoomSerializer, TariffSerializer, SubscriptionSerializer, UserSubscriptionSerializer, \
    BookingSerializer
from .permissions import CoworkingPermission
from .tasks import send_booking_confirmation
import stripe
from django.conf import settings

# Create your views here.
stripe.api_key = settings.STRIPE_SECRET_KEY


class BaseCRUDViewSet(viewsets.ModelViewSet):
    permission_classes = [CoworkingPermission]
    cache_timeout = 60 * 5

    def list(self, request, *args, **kwargs):
        user_id = request.user.id if request.user.is_authenticated else "anon"
        cache_key = f"{self.__class__.__name__}:list:user:{user_id}:{request.get_full_path()}"
        data = cache.get(cache_key)

        if not data:
            response = super().list(request, *args, **kwargs)
            cache.set(cache_key, response.data, self.cache_timeout)
            return response

        return Response(data)

    def retrieve(self, request, *args, **kwargs):
        user_id = request.user.id if request.user.is_authenticated else "anon"
        pk = kwargs.get("pk")
        cache_key = f"{self.__class__.__name__}:detail:{pk}:user:{user_id}"
        data = cache.get(cache_key)

        if not data:
            response = super().retrieve(request, *args, **kwargs)
            cache.set(cache_key, response.data, self.cache_timeout)
            return response

        return Response(data)

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        self._clear_cache()
        return response

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        self._clear_cache()
        return response

    def destroy(self, request, *args, **kwargs):
        response = super().destroy(request, *args, **kwargs)
        self._clear_cache()
        return response

    def _clear_cache(self):
        cache.delete(f"{self.__class__.__name__}:list")
        keys = cache.keys(f"{self.__class__.__name__}:detail:*")
        for key in keys:
            cache.delete(key)


class RoomView(BaseCRUDViewSet):
    """
    API для управления комнатами коворкинга.

    list:
    Получить список всех комнат.

    retrieve:
    Получить данные конкретной комнаты по ID.

    create:
    Добавить новую комнату (для сотрудников).

    update:
    Полностью обновить данные комнаты.

    partial_update:
    Частично обновить данные комнаты.

    destroy:
    Удалить комнату.
    """
    queryset = Room.objects.all().order_by('id')
    serializer_class = RoomSerializer


class TariffView(BaseCRUDViewSet):
    """
    API для тарифов.

    list:
    Получить список тарифов.

    retrieve:
    Получить данные тарифа по ID.

    create:
    Добавить новый тариф.

    update:
    Полностью обновить тариф.

    partial_update:
    Частично обновить тариф.

    destroy:
    Удалить тариф.
    """
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer


class SubscriptionView(BaseCRUDViewSet):
    """
    API для подписок.

    list:
    Получить список подписок.

    retrieve:
    Получить подписку по ID.

    create:
    Создать новую подписку.

    update:
    Обновить подписку.

    partial_update:
    Частично обновить подписку.

    destroy:
    Удалить подписку.
    """
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer

    @action(detail=True, methods=["post"])
    def checkout(self, request, pk=None):
        subscription = self.get_object()

        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            mode='payment',
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': subscription.title,
                        },
                        'unit_amount': int(subscription.price * 100),
                    },
                    'quantity': 1,
                }
            ],
            metadata={
                "user_id": request.user.id,
                "subscription_id": subscription.id
            },
            success_url='http://localhost:8080/profile',
            cancel_url="http://localhost:8080/",
        )

        return Response({"checkout_url": session.url})


class UserSubscriptionView(BaseCRUDViewSet):
    """
    API для пользовательских подписок.

    list:
    Получить список подписок пользователя (или всех для администратора).

    retrieve:
    Получить конкретную подписку пользователя.

    create:
    Добавить подписку текущему пользователю.

    update:
    Обновить подписку пользователя.

    partial_update:
    Частично обновить подписку.

    destroy:
    Удалить подписку.
    """
    queryset = UserSubscription.objects.all().order_by('id')
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return UserSubscription.objects.all().order_by('id')
        if user.is_authenticated:
            return UserSubscription.objects.filter(user=user)
        return UserSubscription.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BookingView(BaseCRUDViewSet):
    """
    API для бронирований.

    list:
    Получить список бронирований (для пользователя или всех — если админ).

    retrieve:
    Получить данные конкретного бронирования.

    create:
    Создать новое бронирование.

    update:
    Обновить бронирование.

    partial_update:
    Частично обновить бронирование.

    destroy:
    Удалить бронирование.
    """
    queryset = Booking.objects.all().order_by('id')
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_superuser or user.is_staff:
            return Booking.objects.all().order_by('id')
        if user.is_authenticated:
            return Booking.objects.filter(user=user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        """
        При создании бронирования запускается Celery-задача
        для отправки email с подтверждением.
        """
        booking = serializer.save()
        send_booking_confirmation.delay(booking.id)

    @action(detail=False, methods=["post"])
    def checkout(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Создаём бронь в памяти (но пока не сохраняем в БД)
        booking = Booking(
            user=request.user,
            room=serializer.validated_data["room"],
            start_time=serializer.validated_data["start_time"],
            end_time=serializer.validated_data["end_time"],
            subscription=serializer.validated_data.get("subscription"),
        )
        if not booking.subscription:
            active_sub = UserSubscription.objects.filter(
                user=request.user,
                start_date__lte=timezone.now().date(),
                end_date__gte=timezone.now().date()
            ).first()
            if active_sub:
                booking.subscription = active_sub

        booking.full_clean()
        price = booking.calculate_price()

        # Если подписка → сохраняем бронь сразу без оплаты
        if price == 0:
            booking.price = 0
            booking.save()
            send_booking_confirmation.delay(booking.id)
            return Response({"message": "Бронирование бесплатно по подписке"}, status=status.HTTP_201_CREATED)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            line_items=[{
                "price_data": {
                    "currency": "usd",
                    "product_data": {"name": f"Бронирование: {booking.room.title}"},
                    "unit_amount": int(price * 100),
                },
                "quantity": 1,
            }],
            metadata={
                "user_id": request.user.id,
                "room_id": booking.room.id,
                "start_time": booking.start_time.isoformat(),
                "end_time": booking.end_time.isoformat(),
            },
            success_url="http://localhost:8080/profile",
            cancel_url="http://localhost:8080/",
        )

        return Response({"checkout_url": session.url})
