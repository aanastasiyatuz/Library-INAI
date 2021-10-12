from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=150)
    book_id = models.PositiveIntegerField()

class Order(models.Model):
    student = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="orders")
    book = models.OneToOneField(Book, related_name="order", on_delete=models.DO_NOTHING)
    dateOfIssue = models.DateField(auto_now_add=True)
    returnDate = models.DateField(blank=True, null=True)
