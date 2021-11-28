from celery import shared_task
from .models import Order
from datetime import date
from .utils import send_email

@shared_task
def check_and_send_email():
    for order in Order.objects.filter(is_returned=False):
        if (date.today() - order.dateOfIssue).days > 90:
            send_email(order.student.email, f"Верните книгу {order.book.title} в библеотеку. Вы ее брали {order.dateOfIssue}")
        elif (date.today() - order.dateOfIssue).days > 60:
            send_email(order.student.email, f"Вы читаете книгу {order.book.title}. Вы ее брали {order.dateOfIssue}. Уже прошло 2 месяца, не забудьте ее вернуть, как дочитаете")
