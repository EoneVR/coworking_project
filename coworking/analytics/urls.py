from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()

router.register(r'analytics_for_bookshop', AnalyticsBookshopView, basename='analytics_for_bookshop')
router.register(r'analytics_for_coworking', AnalyticsCoworkingView, basename='analytics_for_coworking')

urlpatterns = [
    path('', include(router.urls)),
]

