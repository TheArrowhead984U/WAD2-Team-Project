from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from melodyMeter.forms import UserForm, UserProfileForm

# Create your views here.

def index(request):
    context_dict = {'boldmessage': 'Whoopydoo!'}
    return render(request, 'melodyMeter/index.html', context=context_dict)

def albums(request):
    return render(request, 'melodyMeter/albums.html')

@login_required
def profile(request):
    return render(request, 'melodyMeter/profile.html')

@login_required
def addalbum(request):
    return HttpResponse("Add Album")

def signup(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES['picture']:
                profile.picture = request.FILES['picture']

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, 'melodyMeter/signup.html', context={'user_form': user_form,
                                                                     'profile_form': profile_form,
                                                                     'registered': registered})

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('melodyMeter:index'))
            else:
                return HttpResponse("Your MelodyMeter account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'melodyMeter/login.html')
