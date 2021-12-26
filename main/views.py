from django.shortcuts import redirect
from django.urls.base import reverse_lazy

def index(request):
    return redirect(reverse_lazy("books"))