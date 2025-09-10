from rest_framework import serializers
from .models import *


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ['id', 'description', 'discount']


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = ['id', 'title', 'size', 'ingredients', 'unit_price', 'slug', 'promotion', 'image']


class BakerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bakery
        fields = ['id', 'title', 'ingredients', 'unit_price', 'slug', 'promotion', 'in_stock', 'image']
