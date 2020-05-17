import stripe
stripe.api_key = 'sk_test_siXfiHrL4VMn8eI0dn2bp4dm00nOqNVr5o'


def create():
    session = stripe.checkout.Session.create(
    payment_method_types=['card'],
    line_items=[{
        'price': 'price_HIR6t8zme6x26d',
        'quantity': 1,
    }],
    mode='payment',
    success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
    cancel_url='http://127.0.0.1:8000/cancel',
    )
    return session.id
