from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PromotionView, CoffeeView, BakeryView

router = DefaultRouter()
router.register(r'promotions', PromotionView, basename='promotions')
router.register(r'coffees', CoffeeView, basename='coffees')
router.register(r'bakery', BakeryView, basename='bakery')

urlpatterns = [
    path('', include(router.urls)),
]
