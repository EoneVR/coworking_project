import pytest
from django.contrib.auth.models import User
from coffeeshop.models import Promotion, Coffee, Bakery
from decimal import Decimal


@pytest.mark.django_db
def test_promotion_creation():
    promotion = Promotion.objects.create(
        description='Скидка на кофе',
        discount=10.0
    )

    assert promotion.description == 'Скидка на кофе'
    assert promotion.discount == 10.0
    assert str(promotion) == "Скидка на кофе (10.0%)"


@pytest.mark.django_db
def test_coffee_creation():
    promo = Promotion.objects.create(description='Летняя акция', discount=15.0)
    coffee = Coffee.objects.create(
        title="Latte",
        size="250ml",
        ingredients="Эспрессо, молоко",
        unit_price=Decimal("3.50"),
        slug="latte-250ml",
    )
    coffee.promotion.add(promo)

    assert coffee.title == "Latte"
    assert coffee.size == "250ml"
    assert coffee.unit_price == Decimal("3.50")
    assert promo in coffee.promotion.all()
    assert str(coffee) == "Latte (250ml)"


@pytest.mark.django_db
def test_bakery_creation():
    promo = Promotion.objects.create(description='Сладкая акция', discount=5.0)
    bakery = Bakery.objects.create(
        title="Croissant",
        ingredients="Мука, масло, яйца",
        unit_price=Decimal("2.00"),
        slug="croissant",
        in_stock=15,
    )
    bakery.promotion.add(promo)

    assert bakery.title == "Croissant"
    assert bakery.unit_price == Decimal("2.00")
    assert bakery.in_stock == 15
    assert promo in bakery.promotion.all()
    assert str(bakery) == "Croissant (15 шт.)"
