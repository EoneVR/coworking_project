import pytest
from decimal import Decimal
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from coffeeshop.models import Promotion, Coffee, Bakery


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_superuser(username="admin", password="admin1234")


# -------------------- PromotionView --------------------

@pytest.mark.django_db
def test_promotion_list(api_client, admin_user):
    Promotion.objects.create(description="Test Promo", discount=10.0)
    api_client.force_authenticate(user=admin_user)

    response = api_client.get("/coffee/promotions/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["description"] == "Test Promo"


@pytest.mark.django_db
def test_promotion_retrieve(api_client, admin_user):
    promo = Promotion.objects.create(description="Retrieve Promo", discount=5.0)
    api_client.force_authenticate(user=admin_user)

    response = api_client.get(f"/coffee/promotions/{promo.id}/")
    assert response.status_code == 200
    assert response.data["description"] == "Retrieve Promo"


@pytest.mark.django_db
def test_promotion_create(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    data = {"description": "New Promo", "discount": 15.0}

    response = api_client.post("/coffee/promotions/", data)
    assert response.status_code == 201
    assert Promotion.objects.count() == 1


@pytest.mark.django_db
def test_promotion_update(api_client, admin_user):
    promo = Promotion.objects.create(description="Old Promo", discount=10.0)
    api_client.force_authenticate(user=admin_user)

    data = {"description": "Updated Promo", "discount": 20.0}
    response = api_client.put(f"/coffee/promotions/{promo.id}/", data)
    assert response.status_code == 200
    promo.refresh_from_db()
    assert promo.description == "Updated Promo"


@pytest.mark.django_db
def test_promotion_delete(api_client, admin_user):
    promo = Promotion.objects.create(description="Delete Promo", discount=5.0)
    api_client.force_authenticate(user=admin_user)

    response = api_client.delete(f"/coffee/promotions/{promo.id}/")
    assert response.status_code == 204
    assert Promotion.objects.count() == 0


# -------------------- CoffeeView --------------------

@pytest.mark.django_db
def test_coffee_crud(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    promo = Promotion.objects.create(description="Coffee Promo", discount=10.0)

    # create
    data = {
        "title": "Latte",
        "size": "250ml",
        "ingredients": "Эспрессо, молоко",
        "unit_price": "3.50",
        "slug": "latte-250ml",
        "promotion": [promo.id],
    }
    response = api_client.post("/coffee/coffees/", data)
    assert response.status_code == 201
    coffee_id = response.data["id"]

    # list
    response = api_client.get("/coffee/coffees/")
    assert response.status_code == 200
    assert response.data["results"][0]["title"] == "Latte"

    # retrieve
    response = api_client.get(f"/coffee/coffees/{coffee_id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Latte"

    # update
    update_data = data.copy()
    update_data["title"] = "Cappuccino"
    response = api_client.put(f"/coffee/coffees/{coffee_id}/", update_data)
    assert response.status_code == 200
    assert response.data["title"] == "Cappuccino"

    # delete
    response = api_client.delete(f"/coffee/coffees/{coffee_id}/")
    assert response.status_code == 204
    assert Coffee.objects.count() == 0


# -------------------- BakeryView --------------------

@pytest.mark.django_db
def test_bakery_crud(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    promo = Promotion.objects.create(description="Bakery Promo", discount=5.0)

    # create
    data = {
        "title": "Croissant",
        "ingredients": "Мука, масло",
        "unit_price": "2.50",
        "slug": "croissant",
        "promotion": [promo.id],
        "in_stock": 10,
    }
    response = api_client.post("/coffee/bakery/", data)
    assert response.status_code == 201
    bakery_id = response.data["id"]

    # list
    response = api_client.get("/coffee/bakery/")
    assert response.status_code == 200
    assert response.data["results"][0]["title"] == "Croissant"

    # retrieve
    response = api_client.get(f"/coffee/bakery/{bakery_id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Croissant"

    # partial update
    response = api_client.patch(f"/coffee/bakery/{bakery_id}/", {"in_stock": 20})
    assert response.status_code == 202
    assert response.data["in_stock"] == 20

    # delete
    response = api_client.delete(f"/coffee/bakery/{bakery_id}/")
    assert response.status_code == 204
    assert Bakery.objects.count() == 0
