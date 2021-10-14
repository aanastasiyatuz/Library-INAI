from django.urls import path

from .views import BookList, OrderList, BookDetail, BookCreate, OrderCreate, \
    BookUpdate, OrderUpdate, BookDelete, OrderDelete

urlpatterns = [
    path('', BookList.as_view(), name='books'),
    path('orders/', OrderList.as_view(), name='orders'),
    path('book/<int:id>/', BookDetail, name='book-detail'),
    path('create/book/', BookCreate.as_view(), name='create-book'),
    path('create/order/', OrderCreate.as_view(), name='create-order'),
    path('update/book/<int:id>/', BookUpdate.as_view(), name='update-book'),
    path('update/order/<int:id>/', OrderUpdate.as_view(), name='update-order'),
    path('delete/book/<int:id>/', BookDelete.as_view(), name='delete-book'),
    path('delete/order/<int:id>/', OrderDelete.as_view(), name='delete-order'),
]
