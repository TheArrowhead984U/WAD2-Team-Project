from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from melodyMeter.forms import UserForm, UserProfileForm
from melodyMeter.models import Album, Song
from .models import UserProfile

# Create your views here.

def index(request):
    context_dict = {'boldmessage': 'Whoopydoo!'}
    return render(request, 'melodyMeter/index.html', context=context_dict)

def albums(request):
    album_list = Album.objects.order_by('-name')[:5]

    context_dict = {}
    context_dict['albums'] = album_list

    return render(request, 'melodyMeter/albums.html', context=context_dict)

def show_album(request, album_name_slug):
    context_dict = {}

    try:
        album = Album.objects.get(slug=album_name_slug)

        songs = Song.objects.filter(album=album)

        context_dict['songs'] = songs
        context_dict['album'] = album
    except Album.DoesNotExist:
        context_dict['album'] = None
        context_dict['songs'] = None

    return render(request, 'melodyMeter/album.html', context=context_dict)

@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)  # Retrieve the logged-in user's profile
    context = {
        'user_profile': user_profile
    }
    return render(request, 'melodyMeter/profile.html')

@login_required
def addalbum(request):
    return HttpResponse("Add Album")

@login_required
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)  # Retrieve the user's profile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)  # Or handle as appropriate if the profile doesn't exist

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('melodyMeter:profile')  # Redirect to the profile view with the correct namespace
    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'melodyMeter/edit_profile.html', {'form': form})
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

            if 'picture' in request.FILES:
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
                auth_login(request, user)
                return redirect(reverse('melodyMeter:index'))
            else:
                return HttpResponse("Your MelodyMeter account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'melodyMeter/login.html')
