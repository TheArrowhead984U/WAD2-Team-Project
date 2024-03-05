from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    context_dict = {'boldmessage': 'Whoopydoo!'}
    return render(request, 'melodyMeter/index.html', context=context_dict)

def albums(request):
    return render(request, 'melodyMeter/albums.html')

def login(request):
    return HttpResponse("Log In")

def signup(request):
    return HttpResponse("Sign Up")

def profile(request):
    return render(request, 'melodyMeter/profile.html')

def addalbum(request):
    return HttpResponse("Add Album")
