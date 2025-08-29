from django.db import transaction
from django.shortcuts import get_object_or_404
from ..models import Order, OrderItem, Cart


class OrderService:
    @staticmethod
    def create_order_from_cart(user, cart_id):
        cart = get_object_or_404(Cart, id=cart_id, user=user)
        if not cart.items.exists():
            raise ValueError("Корзина пуста")
        with transaction.atomic():
            order = Order.objects.create(customer=user)

            order_items = [
                OrderItem(
                    order=order,
                    book=item.book,
                    quantity=item.quantity,
                    unit_price=item.book.unit_price,
                )
                for item in cart.items.all()
            ]
            OrderItem.objects.bulk_create(order_items)

            cart.items.all().delete()
            return order
