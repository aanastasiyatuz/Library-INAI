from django import forms
from .models import Book, Order, Comment, Rating


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = '__all__'

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]
    
    def save(self, request, book):
        comment = self.instance
        comment.student = request.user
        comment.book = book
        return super().save()

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['rating',]
    
    def save(self, request, book):
        comment = self.instance
        comment.student = request.user
        comment.book = book
        return super().save()