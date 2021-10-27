from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView

from .models import Book, Order, Comment, Rating
from .forms import BookForm, CommentForm, RatingForm
from .permissions import IsAdminPermission

User = get_user_model()


"""--------LIST---------"""
class BookList(ListView):
    model = Book
    template_name = 'books.html'
    paginate_by = 10
    context_object_name = 'books'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        search = self.request.GET.get('q')

        if search and search != 'available':
            context['books'] = Book.objects.filter(title__icontains=search)
        if search == 'available':
            context['books'] = Book.objects.filter(is_available=True)

        return context

class OrderList(LoginRequiredMixin,ListView):
    model = Order
    template_name = 'orders.html'
    paginate_by = 10
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        context['orders'] = Order.objects.filter(student=user)

        search = self.request.GET.get('q')
        if search:
            context['orders'] = context['orders'].filter(book__title__icontains=search)
        
        return context


"""--------DETAIL---------"""
def BookDetail(request, id):
    book = get_object_or_404(Book, id=id)

    # all comments
    comments = Comment.objects.filter(book=book)

    if isinstance(request.user, User):
        my_rating_list = Rating.objects.filter(book=book, student=request.user)
        my_rating = my_rating_list[0] if my_rating_list else None

        if request.method == "POST":
            if len(request.POST) == 1:
                Order.objects.create(student=request.user, book=book)
                book.is_available = False
                book.save()
                return redirect(reverse_lazy('book-detail', kwargs={"id":id}))

            if request.POST.get("body"):
                # add comment
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment_form.save(request, book)
                    return redirect(reverse_lazy('book-detail', kwargs={"id":id}))

            elif request.POST.get("rating"):          
                # add rating
                rating_form = RatingForm(request.POST)
                if rating_form.is_valid():
                    rating_form.save(request, book)
                    return redirect(reverse_lazy('book-detail', kwargs={"id":id}))

        else:
            comment_form = CommentForm()
            rating_form = RatingForm()

        return render(request, 'book-detail.html', {'book':book, 
                                                    'comment_form':comment_form, 
                                                    'comments':comments, 
                                                    'rating_form':rating_form,
                                                    'my_rating':my_rating})
    return render(request, "book-detail.html", {"book":book, "comments":comments})


"""--------CREATE---------"""
class BookCreate(CreateView):
    model = Book
    template_name = 'add-book.html'
    form_class = BookForm
    success_url = reverse_lazy('books')        
    permission_classes = [IsAdminPermission, ]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book_form'] = self.get_form(self.get_form_class())
        return context


"""--------UPDATE---------"""
class BookUpdate(UpdateView):
    model = Book
    template_name = 'update-book.html'
    form_class = BookForm
    success_url = 'books.html'
    pk_url_kwarg = 'id'
    permission_classes = [IsAdminPermission, ]


"""--------DELETE---------"""
class BookDelete(DeleteView):
    model = Book
    template_name = 'delete-book.html'
    success_url = reverse_lazy('books')
    permission_classes = [IsAdminPermission, ]
    pk_url_kwarg = 'id'
