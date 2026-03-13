import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course):
    product = stripe.Product.create(
        name=course.title,
        description=course.description,
    )
    return product["id"]


def create_stripe_price(product_id, amount):
    price = stripe.Price.create(
        unit_amount=int(amount * 100),
        currency="usd",
        product=product_id,
    )
    return price["id"]


def create_checkout_session(price_id):
    session = stripe.checkout.Session.create(
        payment_method_types=["card"],
        line_items=[
            {
                "price": price_id,
                "quantity": 1,
            }
        ],
        mode="payment",
        success_url="http://localhost:8000/payment/success/",
        cancel_url="http://localhost:8000/payment/cancel/",
    )
    return session["url"]
