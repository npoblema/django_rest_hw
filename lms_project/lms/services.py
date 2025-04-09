import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_stripe_product(course):
    """Создание продукта в Stripe."""
    product = stripe.Product.create(
        name=course.title,
        description=course.description or f"Курс {course.title}"
    )
    return product['id']

def create_stripe_price(course, product_id):
    """Создание цены для продукта в Stripe."""
    price = stripe.Price.create(
        unit_amount=int(course.price * 100),  # Цена в копейках
        currency='rub',
        product=product_id,
    )
    return price['id']

def create_stripe_checkout_session(payment):
    """Создание сессии оплаты в Stripe."""
    price_id = create_stripe_price(payment.course, create_stripe_product(payment.course))
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price': price_id,
            'quantity': 1,
        }],
        mode='payment',
        success_url='http://localhost:8000/api/payment/success/',
        cancel_url='http://localhost:8000/api/payment/cancel/',
        metadata={'payment_id': payment.id}
    )
    return {
        'session_id': session['id'],
        'payment_url': session['url']
    }