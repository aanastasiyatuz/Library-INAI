from django.contrib.auth.models import Group
from django.http.response import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from rest_framework.views import APIView
from django.views.generic import CreateView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.views import LoginView
from rest_framework.generics import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth import authenticate, login

from .forms import RegistrationForm
from .utils import send_activation_email

User = get_user_model()


class RegisterView(SuccessMessageMixin, CreateView):
    model = User
    template_name = 'register.html'
    form_class = RegistrationForm
    success_url = reverse_lazy('activate')
    success_message = 'Successfully registered'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['registration_form'] = self.get_form(self.get_form_class())
        return context

def activate_message(request):
    return render(request, "activate-message.html")

def activate_account(request, activation_code):
    user = get_object_or_404(User, activation_code=activation_code)
    user.is_active = True
    user.activation_code = ''
    user.save()
    auth = authenticate(email=user.email, password=user.get__password())
    if auth:
        login(request, auth)
        user.s_password = ''
        user.save()
        return redirect(reverse_lazy("books"))
    else:
        user = User.objects.get(email=user.email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_email(email=user.email, activation_code=user.activation_code)
        return redirect(reverse_lazy("activate"))

class SignInView(LoginView):
    template_name = 'login.html'
    success_url = reverse_lazy('books')
    success_message = 'Successfully login'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['login_form'] = self.get_form(self.get_form_class())
        return context

