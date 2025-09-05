import pytest
from django.contrib.auth.models import User
from coffeeshop.models import Promotion, Coffee, Bakery
from coffeeshop.serializers import PromotionSerializer, CoffeeSerializer, BakerySerializer
from rest_framework.test import APIRequestFactory
from decimal import Decimal


@pytest.mark.django_db
def test_promotion_serializer():
    promo = Promotion.objects.create(description="Зимняя скидка", discount=20.0)
    serializer = PromotionSerializer(promo)

    assert serializer.data["description"] == "Зимняя скидка"
    assert serializer.data["discount"] == 20.0

    # Тест десериализации
    data = {"description": "Весенняя акция", "discount": 15.0}
    serializer = PromotionSerializer(data=data)
    assert serializer.is_valid()
    promo_obj = serializer.save()
    assert promo_obj.description == "Весенняя акция"
    assert promo_obj.discount == 15.0


@pytest.mark.django_db
def test_coffee_serializer():
    promo = Promotion.objects.create(description="На латте", discount=10.0)
    coffee = Coffee.objects.create(
        title="Latte",
        size="250ml",
        ingredients="Эспрессо, молоко",
        unit_price=Decimal("3.50"),
        slug="latte-250ml",
    )
    coffee.promotion.add(promo)

    serializer = CoffeeSerializer(coffee)
    assert serializer.data["title"] == "Latte"
    assert serializer.data["size"] == "250ml"
    assert serializer.data["unit_price"] == 3.50  # Decimal сериализуется в строку
    assert promo.id in serializer.data["promotion"]

    # Тест десериализации
    data = {
        "title": "Cappuccino",
        "size": "200ml",
        "ingredients": "Эспрессо, молоко, пена",
        "unit_price": "4.00",
        "slug": "cappuccino-200ml",
        "promotion": [promo.id],
    }
    serializer = CoffeeSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    coffee_obj = serializer.save()
    assert coffee_obj.title == "Cappuccino"
    assert promo in coffee_obj.promotion.all()


@pytest.mark.django_db
def test_bakery_serializer():
    promo = Promotion.objects.create(description="На круассан", discount=5.0)
    bakery = Bakery.objects.create(
        title="Croissant",
        ingredients="Мука, масло, яйца",
        unit_price=Decimal("2.50"),
        slug="croissant",
        in_stock=10,
    )
    bakery.promotion.add(promo)

    serializer = BakerySerializer(bakery)
    assert serializer.data["title"] == "Croissant"
    assert serializer.data["in_stock"] == 10
    assert serializer.data["unit_price"] == 2.50
    assert promo.id in serializer.data["promotion"]

    # Тест десериализации
    data = {
        "title": "Donut",
        "ingredients": "Мука, сахар, глазурь",
        "unit_price": "1.50",
        "slug": "donut",
        "promotion": [promo.id],
        "in_stock": 25,
    }
    serializer = BakerySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    bakery_obj = serializer.save()
    assert bakery_obj.title == "Donut"
    assert bakery_obj.in_stock == 25
    assert promo in bakery_obj.promotion.all()