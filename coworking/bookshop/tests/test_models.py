import pytest
from django.contrib.auth.models import User
from bookshop.models import Category, Book, Cart, CartItem, Order, OrderItem
from decimal import Decimal


@pytest.mark.django_db
def test_creation_category():
    category = Category.objects.create(title='test category')

    assert category.title == 'test category'


@pytest.mark.django_db
def test_creation_book():
    category = Category.objects.create(title='Бизнес литература')
    book = Book.objects.create(
        title='Clean Code',
        description='Классика программирования',
        author='Robert Martin',
        unit_price=Decimal("29.99"),
        year_of_publish=2008,
        pages=464,
        binding=Book.Binding.HARD,
        in_stock=10,
        category=category,
    )

    assert book.title == 'Clean Code'
    assert book.author == 'Robert Martin'
    assert str(book) == "Clean Code — Robert Martin"


@pytest.mark.django_db
def test_cart_and_cartitem():
    user = User.objects.create_user(username="testuser", password="1234")
    category = Category.objects.create(title='IT')
    book = Book.objects.create(
        title='The Pragmatic Programmer',
        description='Guide for developers',
        author='Andrew Hunt',
        unit_price=Decimal("50.00"),
        year_of_publish=1999,
        pages=352,
        category=category,
    )
    cart = Cart.objects.create(user=user)
    item = CartItem.objects.create(cart=cart, book=book, quantity=2)

    assert str(cart).startswith("Корзина")
    assert item.total_price == Decimal("100.00")
    assert cart.total_price == Decimal("100.00")


@pytest.mark.django_db
def test_order_and_orderitem():
    user = User.objects.create_user(username="buyer", password="1234")
    category = Category.objects.create(title='Фантастика')
    book = Book.objects.create(
        title='Dune',
        description='Sci-Fi classic',
        author='Frank Herbert',
        unit_price=Decimal("15.00"),
        year_of_publish=1965,
        pages=500,
        category=category,
    )
    order = Order.objects.create(customer=user)
    order_item = OrderItem.objects.create(
        order=order,
        book=book,
        quantity=3,
        unit_price=book.unit_price,
    )

    assert str(order).startswith("Заказ")
    assert order.payment_status == Order.PaymentStatus.PENDING
    assert order_item.quantity == 3
    assert order_item.unit_price == Decimal("15.00")
