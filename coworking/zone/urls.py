from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RoomView, TariffView, SubscriptionView, UserSubscriptionView, BookingView

router = DefaultRouter()
router.register(r'rooms', RoomView, basename='rooms')
router.register(r'tariffs', TariffView, basename='tariffs')
router.register(r'subscriptions', SubscriptionView, basename='subscriptions')
router.register(r'usersubscriptions', UserSubscriptionView, basename='usersubscriptions')
router.register(r'bookings', BookingView, basename='bookings')


urlpatterns = [
    path('', include(router.urls)),
]
