from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, DeleteView, UpdateView
from django.views.generic.detail import DetailView

from .models import Book, Order, Comment
from .forms import BookForm, OrderForm, CommentForm, RatingForm
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

class OrderList(ListView):
    model = Order
    template_name = 'orders.html'
    paginate_by = 10
    context_object_name = 'orders'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if not isinstance(user, User):
            redirect('login.html')

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

    if request.method == "POST":
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
                                                'rating_form':rating_form})


"""--------CREATE---------"""
class BookCreate(CreateView):
    model = Book
    template_name = 'add-book.html'
    form_class = BookForm
    success_url = reverse_lazy('books')        
    permission_classes = [IsAdminPermission, ]

class OrderCreate(CreateView):
    model = Order
    template_name = 'add-order.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders')

    def form_valid(self, form):
        user = self.request.user
        order = form.save(commit=False)
        order.student = user
        order.save()
        return super().form_valid(form)


"""--------UPDATE---------"""
class BookUpdate(UpdateView):
    model = Book
    template_name = 'update-book.html'
    form_class = BookForm
    success_url = 'books.html'
    pk_url_kwarg = 'id'
    permission_classes = [IsAdminPermission, ]

class OrderUpdate(UpdateView):
    model = Order
    template_name = 'update-order.html'
    form_class = OrderForm
    success_url = 'orders.html'
    pk_url_kwarg = 'id'
    permission_classes = [IsAdminPermission, ]


"""--------DELETE---------"""
class BookDelete(DeleteView):
    model = Book
    template_name = 'delete-book.html'
    success_url = reverse_lazy('books')
    permission_classes = [IsAdminPermission, ]
    pk_url_kwarg = 'id'

class OrderDelete(DeleteView):
    model = Order
    template_name = 'delete-order.html'
    success_url = reverse_lazy('orders')
    permission_classes = [IsAdminPermission, ]
    pk_url_kwarg = 'id'
