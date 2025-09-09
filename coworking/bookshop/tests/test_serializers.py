import pytest
from django.contrib.auth.models import User
from bookshop.models import Category, Book, Cart, CartItem, Order, OrderItem
from bookshop.serializers import CategorySerializer, BookSerializer, CartSerializer, CartItemSerializer, \
    OrderSerializer, OrderItemSerializer
from datetime import date
from decimal import Decimal


@pytest.mark.django_db
def test_category_serializer():
    category = Category.objects.create(title="Фантастика")
    serializer = CategorySerializer(category)
    data = serializer.data

    assert data["id"] == category.id
    assert data["title"] == "Фантастика"


@pytest.mark.django_db
def test_book_serializer():
    category = Category.objects.create(title="IT")
    book = Book.objects.create(
        title="Clean Code",
        description="Best practices",
        author="Robert Martin",
        unit_price=Decimal("25.50"),
        year_of_publish=2008,
        pages=464,
        binding=Book.Binding.HARD,
        in_stock=10,
        category=category,
    )
    serializer = BookSerializer(book)
    data = serializer.data

    assert data["title"] == "Clean Code"
    assert data["author"] == "Robert Martin"
    assert data["unit_price"] == 25.50
    assert data["category"] == category.id


@pytest.mark.django_db
def test_cartitem_serializer():
    user = User.objects.create_user(username="testuser", password="1234")
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
    cart = Cart.objects.create(user=user)
    cart_item = CartItem.objects.create(cart=cart, book=book, quantity=2)

    serializer = CartItemSerializer(cart_item)
    data = serializer.data

    assert data["book"]["title"] == "Refactoring"
    assert data["quantity"] == 2
    assert Decimal(data["total_price"]) == Decimal("60.00")
    assert data["book_id"]


@pytest.mark.django_db
def test_cart_serializer():
    user = User.objects.create_user(username="cartuser", password="1234")
    category = Category.objects.create(title="Programming")
    book = Book.objects.create(
        title="Design Patterns",
        description="Classic GoF book",
        author="GoF",
        unit_price=Decimal("40.00"),
        year_of_publish=1994,
        pages=395,
        category=category,
    )
    cart = Cart.objects.create(user=user)
    CartItem.objects.create(cart=cart, book=book, quantity=3)

    serializer = CartSerializer(cart)
    data = serializer.data

    assert data["id"] == str(cart.id)
    assert Decimal(data["total_price"]) == Decimal("120.00")
    assert len(data["items"]) == 1


@pytest.mark.django_db
def test_orderitem_serializer():
    user = User.objects.create_user(username="buyer", password="1234")
    category = Category.objects.create(title="Sci-Fi")
    book = Book.objects.create(
        title="Dune",
        description="Epic saga",
        author="Frank Herbert",
        unit_price=Decimal("15.00"),
        year_of_publish=1965,
        pages=500,
        category=category,
    )
    order = Order.objects.create(customer=user)
    order_item = OrderItem.objects.create(order=order, book=book, quantity=2, unit_price=book.unit_price)

    serializer = OrderItemSerializer(order_item)
    data = serializer.data

    assert data["book"] == book.id
    assert data["book_title"] == "Dune"
    assert data["quantity"] == 2
    assert Decimal(data["total_price"]) == Decimal("30.00")


@pytest.mark.django_db
def test_order_serializer():
    user = User.objects.create_user(username="orderuser", password="1234")
    category = Category.objects.create(title="Fantasy")
    book = Book.objects.create(
        title="LOTR",
        description="Epic fantasy",
        author="J.R.R. Tolkien",
        unit_price=Decimal("20.00"),
        year_of_publish=1954,
        pages=1000,
        category=category,
    )
    order = Order.objects.create(customer=user)
    OrderItem.objects.create(order=order, book=book, quantity=3, unit_price=book.unit_price)

    serializer = OrderSerializer(order)
    data = serializer.data

    assert data["customer"] == user.id
    assert data["payment_status"] == "P"
    assert Decimal(data["total_price"]) == Decimal("60.00")
    assert len(data["items"]) == 1
