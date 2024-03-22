from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from melodyMeter.forms import UserForm, UserProfileForm, AlbumForm
from melodyMeter.models import Album, Song, SongRating, UserProfile
import json
from ytmusicapi import YTMusic

# Create your views here.

def index(request):
    context_dict = {'boldmessage': 'Whoopydoo!'}
    return render(request, 'melodyMeter/index.html', context=context_dict)


def albums(request):
    album_list = Album.objects.order_by('-rating')

    context_dict = {}
    context_dict['albums'] = album_list

    return render(request, 'melodyMeter/albums.html', context=context_dict)


def show_album(request, album_name_slug):
    context_dict = {}

    try:
        album = Album.objects.get(slug=album_name_slug)

        songs = Song.objects.filter(album=album)
        song_ratings = []

        if request.user.is_authenticated:
            for song in songs:
                try:
                    song_rating = SongRating.objects.get(song=song, user=request.user)
                    song_ratings.append((song, song_rating.rating))
                except SongRating.DoesNotExist:
                    song_ratings.append((song, 0))
            print(song_ratings)
        else:
            song_ratings = [(song, 0) for song in songs]
        

        context_dict['album'] = album
        context_dict['songs'] = song_ratings
        context_dict['userRating'] = (round(sum([rating[1] for rating in song_ratings])/len(song_ratings), 2))
        print(context_dict['userRating'])
    except Album.DoesNotExist:
        context_dict['album'] = None
        context_dict['songs'] = None
        context_dict['userRating']= None

    return render(request, 'melodyMeter/album.html', context=context_dict)


@login_required
def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    user_ratings = SongRating.objects.filter(user=request.user)
    albRatings = {}
    for rating in user_ratings:
        albRatings.update({rating.song.album: (albRatings[rating.song.album] if rating.song.album in albRatings.keys() else [])+[rating.rating]})

    for alb in albRatings:
        albRatings[alb] = round(sum(albRatings[alb]) / len(albRatings[alb]), 2)

    sorted_alb = dict(sorted(albRatings.items(), key=lambda item: item[1], reverse=True))

    albRatings = tuple(sorted_alb.items())[:5]
    print(albRatings[:5])


    context_dict = {}
    context_dict['user_profile'] = user_profile
    context_dict['alb_ratings'] = albRatings
    return render(request, 'melodyMeter/profile.html', context=context_dict)

@login_required
def edit_profile(request):
    try:
        user_profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('melodyMeter:profile')

    else:
        form = UserProfileForm(instance=user_profile)

    return render(request, 'melodyMeter/edit_profile.html', {'form': form})

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


def logout(request):
    auth_logout(request)
    return redirect(reverse('melodyMeter:index'))


def get_alert_contents(request):
    ytmusic = YTMusic()
    res = ytmusic.search(request.GET.get('artist') + ' ' + request.GET.get('song_id'))
    for i in range(len(res)):
        if res[i]['resultType'] == "song":
            break
    song = ytmusic.get_watch_playlist(res[i]['videoId'])
    alert_contents = ytmusic.get_lyrics(song['lyrics'])['lyrics']

    return JsonResponse({'alert_contents':alert_contents})

def calcAlbumRating(album):
    songs = Song.objects.filter(album=album)

    totalRating = 0
    noSongsRated = 0

    for song in songs:
        ratings = SongRating.objects.filter(song=song)

        if ratings:
            avgRating = ratings.aggregate(Avg('rating'))['rating__avg']
            if avgRating is not None:
                totalRating += avgRating
                noSongsRated += 1
    if noSongsRated > 0:
        albAvg = totalRating / noSongsRated
        album.rating = albAvg
        album.save()
        print(albAvg)

@login_required
def rate_song(request, album_name_slug, song_id):
    if request.method == 'POST':
        song = get_object_or_404(Song, id=song_id)
        rating = request.POST.get(str(song_id) + '_rating')
        if rating:
            ratingObj, created = SongRating.objects.get_or_create(song=song, user=request.user)
            ratingObj.rating = rating
            ratingObj.save()
            calcAlbumRating(Album.objects.get(slug=album_name_slug))
            return redirect(reverse('melodyMeter:show_album', args=[album_name_slug]))
        else:
            return HttpResponse('No raing provided!', status=400)
    else:
        return HttpResponseNotAllowed(['POST'])
