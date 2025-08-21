from rest_framework import serializers
from .models import *


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'


class CoffeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coffee
        fields = '__all__'


class BakerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Bakery
        fields = '__all__'
