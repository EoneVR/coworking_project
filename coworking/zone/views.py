from rest_framework import viewsets
from rest_framework.response import Response
from django.core.cache import cache
from .models import *
from .serializers import RoomSerializer, TariffSerializer, SubscriptionSerializer, UserSubscriptionSerializer, \
    BookingSerializer
from .permissions import CoworkingPermission
from .tasks import send_booking_confirmation

# Create your views here.

class BaseCRUDViewSet(viewsets.ModelViewSet):
    permission_classes = [CoworkingPermission]
    cache_timeout = 60 * 5  # 5 минут

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
        """Чистим кеш списка и деталей"""
        cache.delete(f"{self.__class__.__name__}:list")
        keys = cache.keys(f"{self.__class__.__name__}:detail:*")
        for key in keys:
            cache.delete(key)


class RoomView(BaseCRUDViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class TariffView(BaseCRUDViewSet):
    queryset = Tariff.objects.all()
    serializer_class = TariffSerializer


class SubscriptionView(BaseCRUDViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer


class UserSubscriptionView(BaseCRUDViewSet):
    queryset = UserSubscription.objects.all()
    serializer_class = UserSubscriptionSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return UserSubscription.objects.all()
        if user.is_authenticated:
            return UserSubscription.objects.filter(user=user)
        return UserSubscription.objects.none()

    def perform_create(self, serializer):
        # пользователь — текущий user
        serializer.save(user=self.request.user)


class BookingView(BaseCRUDViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Booking.objects.all()
        if user.is_authenticated:
            return Booking.objects.filter(user=user)
        return Booking.objects.none()

    def perform_create(self, serializer):
        # serializer.create() сам использует request.user из context, но на всякий случай:
        booking = serializer.save()
        send_booking_confirmation.delay(booking.id)
