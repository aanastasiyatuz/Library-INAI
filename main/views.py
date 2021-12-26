from django.shortcuts import redirect, render
from django.urls.base import reverse_lazy

def index(request):
    return redirect(reverse_lazy("books"))

def qr(request):
    return render(request, 'qr.html')