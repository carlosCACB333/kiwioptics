from django.shortcuts import render
from django.contrib.auth.models import User

# Create your views here.
def signup(request):
    return render(request, 'users/signup.html')

def login(request):
    return render(request, 'users/login.html')