from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from melodyMeter.forms import UserForm, UserProfileForm, AlbumForm
from melodyMeter.models import Album, Song
import azapi
import json
from ytmusicapi import YTMusic

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
    return render(request, 'melodyMeter/profile.html')

@login_required
def add_album(request):
    form = AlbumForm()

    if request.method == 'POST':
        print('Made it to view')
        form = AlbumForm(request.POST, request.FILES)
        if form.is_valid():
            album_instance = form.save(commit=False)
            album_instance.name = ' '.join([x.capitalize() for x in album_instance.name.split()])
            album_instance.artist = ' '.join([x.capitalize() for x in album_instance.artist.split()])
            ytmusic = YTMusic()
            res = ytmusic.search(album_instance.artist + ' ' + album_instance.name)
            for i in range(len(res)):
                if res[i]['resultType'] == "album":
                    break
            alb = ytmusic.get_album(res[i]['browseId'])
            songs = alb['tracks']
            for song in list(songs):
                print(song['title']) 
            print('Success')
            album_instance.cover = request.FILES['cover']
            album_instance.year = alb['year']
            album_instance.save() 
            for song in songs:
                Song.objects.create(album=album_instance, name=song['title'], length=song['duration'])
            #form.save(commit=True)
            return redirect('/melodyMeter/albums/'+album_instance.slug)
        else:
            print('Error with form')
            print(form.errors)
    return render(request, 'melodyMeter/addalbum.html', {'form': form})

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

def get_alert_contents(request):
    api = azapi.AZlyrics()
    
    #api.artist = request.GET.get('artist')
    #api.title = request.GET.get('song_id')
    #api.getLyrics()

    ytmusic = YTMusic()
    res = ytmusic.search(request.GET.get('artist') + ' ' + request.GET.get('song_id'))
    for i in range(len(res)):
        if res[i]['resultType'] == "song":
            break
    song = ytmusic.get_watch_playlist(res[i]['videoId'])
    alert_contents = ytmusic.get_lyrics(song['lyrics'])['lyrics']

    return JsonResponse({'alert_contents':alert_contents})

    #if api.lyrics == '':
    #    alert_contents = "Couldn't find any lyrics for this song."
    #else:
    #    alert_contents = api.lyrics#"This is the generated msg."

    #return JsonResponse({'alert_contents':alert_contents})
