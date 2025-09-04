from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now
from .models import *


@shared_task
def send_booking_confirmation(booking_id):
    booking = Booking.objects.get(id=booking_id)
    send_mail(
        subject=f"Подтверждение бронирования #{booking.id}",
        message=f"Ваше бронирование комнаты {booking.room} подтверждено.",
        from_email='coworking_lounge@.com',
        recipient_list=[booking.user.email],
    )


@shared_task
def check_expired_subscriptions():
    today = now().date()
    expired = UserSubscription.objects.filter(end_date__lt=today)
    for sub in expired:
        send_mail(
            subject="Ваша подписка истекла",
            message=f"Подписка {sub.subscription.title} завершилась {sub.end_date}.",
            from_email="coworking_lounge@.com",
            recipient_list=[sub.user.email],
        )
