from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import RegisterView, SignInView, AdminView


urlpatterns = [
    path('admin', AdminView, name='admin'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
