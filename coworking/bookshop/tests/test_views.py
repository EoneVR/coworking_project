import pytest
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from bookshop.models import Category, Book, Cart, CartItem, Order


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user(db):
    return User.objects.create_user(username="admin", password="1234", is_staff=True)


@pytest.fixture
def regular_user(db):
    return User.objects.create_user(username="testuser", password="1234")


@pytest.mark.django_db
def test_category_crud(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)

    # Create
    response = api_client.post("/books/categories/", {"title": "Фантастика"})
    assert response.status_code == status.HTTP_201_CREATED
    category_id = response.data["id"]

    # List
    response = api_client.get("/books/categories/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["results"][0]["title"] == "Фантастика"

    # Retrieve
    response = api_client.get(f"/books/categories/{category_id}/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Фантастика"

    # Update
    response = api_client.put(f"/books/categories/{category_id}/", {"title": "Sci-Fi"})
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Sci-Fi"

    # Delete
    response = api_client.delete(f"/books/categories/{category_id}/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Category.objects.count() == 0


@pytest.mark.django_db
def test_book_crud(api_client, admin_user):
    api_client.force_authenticate(user=admin_user)
    category = Category.objects.create(title="Programming")

    # Create
    url = "/books/books/"
    data = {
        "title": "Clean Code",
        "description": "Книга о коде",
        "author": "Robert Martin",
        "unit_price": "25.50",
        "year_of_publish": 2008,
        "pages": 464,
        "binding": "hard",
        "in_stock": 5,
        "category": category.id,
    }
    response = api_client.post(url, data, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    book_id = response.data["id"]

    # Retrieve
    url_detail = f"/books/books/{book_id}/"
    response = api_client.get(url_detail)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["title"] == "Clean Code"

    # Partial update
    response = api_client.patch(url_detail, {"in_stock": 10}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["in_stock"] == 10

    # Delete
    response = api_client.delete(url_detail)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Book.objects.count() == 0



@pytest.mark.django_db
def test_cart_actions(api_client, regular_user):
    api_client.force_authenticate(user=regular_user)
    category = Category.objects.create(title="Бизнес")
    book = Book.objects.create(
        title="Refactoring",
        description="Improve design",
        author="Martin Fowler",
        unit_price=Decimal("30.00"),
        year_of_publish=1999,
        pages=400,
        category=category,
    )

    # Add to cart
    url_add = "/books/carts/add_to_cart/"
    response = api_client.post(url_add, {"book_id": book.id, "quantity": 2}, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert CartItem.objects.count() == 1

    # My cart
    url_cart = "/books/carts/my_cart/"
    response = api_client.get(url_cart)
    assert response.status_code == status.HTTP_200_OK
    assert response.data["total_price"] == 60.00

    # Remove from cart
    url_remove = "/books/carts/remove_from_cart/"
    response = api_client.post(url_remove, {"book_id": book.id}, format="json")
    assert response.status_code == status.HTTP_200_OK
    assert CartItem.objects.count() == 0

    # Clear cart
    api_client.post(url_add, {"book_id": book.id, "quantity": 1}, format="json")
    url_clear = "/books/carts/clear_cart/"
    response = api_client.post(url_clear)
    assert response.status_code == status.HTTP_200_OK
    assert CartItem.objects.count() == 0


@pytest.mark.django_db
def test_order_create(api_client, regular_user, mocker):
    api_client.force_authenticate(user=regular_user)
    category = Category.objects.create(title="Фантастика")
    book = Book.objects.create(
        title="Dune",
        description="Sci-Fi saga",
        author="Frank Herbert",
        unit_price=Decimal("15.00"),
        year_of_publish=1965,
        pages=500,
        category=category,
    )

    cart_url = "/books/carts/add_to_cart/"
    api_client.post(cart_url, {"book_id": book.id, "quantity": 2}, format="json")
    cart = Cart.objects.get(user=regular_user)

    mocker.patch(
        "bookshop.views.OrderService.create_order_from_cart",
        return_value=Order.objects.create(customer=regular_user)
    )
    mocker.patch(
        "bookshop.views.PaymentService.create_checkout_session",
        return_value=mocker.Mock(url="http://fake-checkout")
    )
    mocker.patch("bookshop.views.send_order_confirmation.delay", return_value=None)

    url = "/books/orders/"
    response = api_client.post(url, {"cart_id": str(cart.id)}, format="json")
    assert response.status_code == status.HTTP_201_CREATED
    assert "order" in response.data
    assert "checkout_url" in response.data

