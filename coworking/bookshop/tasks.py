from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from .models import Book, Cart, Order
from django.utils.timezone import now, timedelta
import stripe

stripe.api_key = settings.STRIPE_SECRET_KEY


@shared_task
def send_order_confirmation(order_id):
    order = Order.objects.get(id=order_id)
    items = "\n".join(
        [f"{item.book.title} — {item.quantity} шт." for item in order.items.all()]
    )

    send_mail(
        subject=f'Подтверждение заказа №{order.id}',
        message=f"Спасибо за заказ!\n\nВы заказали:\n{items}\n\n"
                f"Сумма: {sum(i.unit_price * i.quantity for i in order.items.all())}$",
        from_email='coworking_lounge@.com',
        recipient_list=[order.customer.email]
    )


@shared_task
def check_payment_status(order_id, session_id):
    order = Order.objects.get(id=order_id)
    session = stripe.checkout.Session.retrieve(session_id)

    if session.payment_status == 'paid':
        order.payment_status = Order.PaymentStatus.COMPLETE
        order.save()

        for item in order.items.select_related('book'):
            if item.book.in_stock >= item.quantity:
                item.book.in_stock -= item.quantity
                item.book.save()
            else:
                raise ValueError(
                    f"Недостаточно книг '{item.book.title}' на складе"
                )
    elif session.payment_status == 'unpaid':
        order.payment_status = Order.PaymentStatus.PENDING
        order.save()
    else:
        order.payment_status = Order.PaymentStatus.FAILED
        order.save()


@shared_task
def clear_old_carts():
    week_ago = now() - timedelta(days=7)
    deleted_count, _ = Cart.objects.filter(
        created_at__lt=week_ago,
        items__isnull=True
    ).delete()
    return f'Удалено {deleted_count} старых пустых корзин'
