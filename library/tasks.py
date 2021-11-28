from celery import shared_task
from .models import Order
from datetime import date
from .utils import send_email

@shared_task
def check_and_send_email():
    for order in Order.objects.filter(is_returned=False):
        print(order)
        order_date = order.dateOfIssue
        if order_date.year != date.year:
            send_email(order.student.email, f"Верните книгу {order.book.title} в библеотеку. Вы ее брали {order_date}")
        