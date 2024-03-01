from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    context_dict = {'boldmessage': 'Whoopydoo!'}
    return render(request, 'melodyMeter/index.html', context=context_dict)

def albums(request):
    return HttpResponse("Albums")

def login(request):
    return HttpResponse("Log In")

def signup(request):
    return HttpResponse("Sign Up")

def profile(request):
    return HttpResponse("Profile")

def addalbum(request):
    return HttpResponse("Add Album")
