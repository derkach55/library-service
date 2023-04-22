import stripe
from django.conf import settings

from borrowing.models import Borrowing
from payment.models import Payment

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_payment(borrowing: Borrowing, session: stripe.checkout.Session):
    Payment.objects.create(
        status='PENDING',
        type='PAYMENT',
        borrowing=borrowing,
        session_url=session.url,
        session_id=session.id,
        money_to_pay=session.amount_total/100
    )


def create_stripe_session(borrowing: Borrowing) -> stripe.checkout.Session:
    amount = int(100 * borrowing.book.fee * (borrowing.expected_return - borrowing.borrow_date).days)
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': borrowing.book.title,
                },
                'unit_amount': amount,
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/success',
        cancel_url='http://localhost:8000/cancel',
    )
    create_payment(borrowing, session)
    return session
