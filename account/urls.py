from django.urls import path
from django.contrib.auth.views import LogoutView

from .views import RegisterView, SignInView, activate_account, activate_message


urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('activate/<str:activation_code>/', activate_account),
    path('login/', SignInView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('activate-message/', activate_message, name='activate')
]
