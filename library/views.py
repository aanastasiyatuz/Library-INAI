from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import CreateView, ListView, DeleteView, UpdateView, DetailView

from .models import Book, Order
from .forms import BookForm, OrderForm
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
class BookDetail(DetailView):
    model = Book
    template_name = 'book-detail.html'
    context_object_name = 'book'
    pk_url_kwarg = 'id'


"""--------CREATE---------"""
class BookCreate(CreateView):
    model = Book
    template_name = 'add-book.html'
    form_class = BookForm
    success_url = reverse_lazy('books.html')        
    permission_classes = [IsAdminPermission, ]

class OrderCreate(CreateView):
    model = Order
    template_name = 'add-order.html'
    form_class = OrderForm
    success_url = reverse_lazy('orders.html')

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
    success_url = reverse_lazy('books.html')
    permission_classes = [IsAdminPermission, ]
    pk_url_kwarg = 'id'

class OrderDelete(DeleteView):
    model = Order
    template_name = 'delete-order.html'
    success_url = reverse_lazy('orders.html')
    permission_classes = [IsAdminPermission, ]
    pk_url_kwarg = 'id'
