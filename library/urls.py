from django.urls import path

from .views import BookList, OrderList, BookDetail, BookCreate,\
    BookUpdate, BookDelete, OrderDelete, AvailableBookList

urlpatterns = [
    path('', BookList.as_view(), name='books'),
    path('available/', AvailableBookList.as_view(), name='available'),
    path('orders/', OrderList.as_view(), name='orders'),
    path('book/<int:id>/', BookDetail, name='book-detail'),
    path('create/book/', BookCreate.as_view(), name='create-book'),
    path('update/book/<int:id>/', BookUpdate.as_view(), name='update-book'),
    path('delete/book/<int:id>/', BookDelete, name='delete-book'),
    path('delete/order/<int:id>/', OrderDelete, name='delete-order'),
]