import stripe
from django.conf import settings
from ..tasks import check_payment_status

stripe.api_key = settings.STRIPE_SECRET_KEY


class PaymentService:
    @staticmethod
    def create_checkout_session(order):
        total_price = sum([oi.unit_price * oi.quantity for oi in order.items.all()])
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price_data": {
                        "currency": "usd",
                        "product_data": {"name": f"Заказ #{order.id}"},
                        "unit_amount": int(total_price * 100),
                    },
                    "quantity": 1,
                }
            ],
            mode="payment",
            success_url="http://localhost:8000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://localhost:8000/cancel",
        )
        check_payment_status.apply_async((order.id, session.id), countdown=300)
        return session

