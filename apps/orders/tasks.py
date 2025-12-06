from celery import shared_task
from django.core.mail import send_mail
from .models import Order

@shared_task
def send_order_created_email(order_id):
    """
    Task to send an e-mail notification when an order is successfully created.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Order nr. {order.id}'
        message = f'Dear {order.first_name},\n\n' \
                  f'You have successfully placed an order.' \
                  f'Your order ID is {order.id}.' \
                  f'Please complete the payment to finalize your order.'
        mail_sent = send_mail(subject,
                              message,
                              'EyeFrame Shop <MS_lT8D8W@test-yxj6lj927554do2r.mlsender.net>',
                              [order.email])
        return mail_sent
    except Order.DoesNotExist:
        return False

@shared_task
def send_payment_success_email(order_id):
    """
    Task to send an e-mail notification when payment is successful.
    """
    try:
        order = Order.objects.get(id=order_id)
        subject = f'Payment Received - Order nr. {order.id}'
        message = f'Dear {order.first_name},\n\n' \
                  f'We have received your payment for order {order.id}.\n' \
                  f'Thank you for shopping with us!'
        mail_sent = send_mail(subject,
                              message,
                              'EyeFrame Shop <MS_lT8D8W@test-yxj6lj927554do2r.mlsender.net>',
                              [order.email])
        return mail_sent
    except Order.DoesNotExist:
        return False
