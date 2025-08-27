from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryView, BookView, CartView, OrderViewSet

router = DefaultRouter()
router.register(r'categories', CategoryView, basename='categories')
router.register(r'books', BookView, basename='books')
router.register(r'carts', CartView, basename='carts')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
]

