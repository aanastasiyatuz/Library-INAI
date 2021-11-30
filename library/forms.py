from django import forms
from .models import Book, Comment, Rating, Order


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
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
        books = Rating.objects.filter(book=book)
        if request.user in [book.student for book in books]:
            obj = Rating.objects.get(book=book, student=request.user).delete()
        rating = self.instance
        rating.student = request.user
        rating.book = book
        return super().save()