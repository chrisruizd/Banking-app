from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    return render(request, 'bank/home.html')

def about(request):
    return render(request, 'bank/about.html')

def login(request):
    return render(request, )

def signup(request):
    return render(request, )

