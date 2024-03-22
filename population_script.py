import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WADProject.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django.core.files import File
from melodyMeter.models import Album, Song, UserProfile, SongRating
from ytmusicapi import YTMusic
import random
from django.db.models import Avg

def clear():
    superuser = User.objects.filter(is_superuser=True).first()
    if superuser:
        User.objects.exclude(username=superuser.username).delete()
        UserProfile.objects.exclude(user=superuser).delete()
        Album.objects.all().delete()
        Song.objects.all().delete()
        SongRating.objects.all().delete()
    else:
        print("No superuser found No action taken")

def populate():

    users = {
            "Bob": {
                "username": "bobTheGOAT_520",
                "email": "",
                "password": "bobbyBoy!"
            },
            "Liz": {
                "username": "lizzyWizzy",
                "email": "lizturnhall@gmail.com",
                "password": "sammy104"
            },
            "Julie": {
                "username": "JulesRulezz",
                "email": "julesshollan@outlook.co.uk",
                "password": "Comtuwar43"
            }
    }

    albums = {
            "Iowa": {
                "artist": "slipknot",
                "image": "iowa.jpg"
            },
            "Thriller": {
                "artist": "michael jackson",
                "image": "thriller.png"
            },
            "Dark Side of the Moon": {
                "artist": "pink floyd",
                "image": "darksideofthemoon.png"
            },
            "Abbey Road": {
                "artist": "the beatles",
                "image": "abbeyroad.jpg"
            },
            "From Under the Cork Tree": {
                "artist": "fall out boy",
                "image": "fromunderthecorktree.jpg"
            },
            "slipknot": {
                "artist": "slipknot",
                "image": "slipknot.jpg"
            },
            "project regeneration vol. 2": {
                "artist": "static-x",
                "image": "projectregeneration.jpg"
            },
            "After Hours": {
                "artist": "The Weeknd",
                "image": "after.jpg"
            },
            "All Or Nothing": {
                "artist": "Jay Sean",
                "image": "jay.jpg"
            }

    }

    albumList = []
    albumsongs = []

    print('Adding Albums')
    for album, albumdata in albums.items():
        a = add_album(album, albumdata['artist'], albumdata['image'])
        albumsongs.append(Song.objects.filter(album=a))
        albumList.append(a)

    u = []

    print('Adding Users')
    for user, userdata in users.items():
        u.append(add_user(user, userdata['username'], userdata['email'], userdata['password'])[0])

    print('Adding User Ratings')
    for user in u:
        sr = add_ratings(user, albumsongs)
        print(user)

    print('Updating Album Averages')
    for album in albumList:
        calcAlbumRating(album)

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

def add_ratings(user, albumsongs):
    for album in albumsongs:
        for song in album:
            SongRating.objects.create(user=user, song=song, rating=random.randint(1,5))

def add_user(name, username, email, password):
    print('\t' + name)
    u = User.objects.create_user(username=username, password=password, email=email)
    u.first_name = name
    up = UserProfile.objects.create(user=u)
    with open('pop-imgs/'+name+'.jpg', 'rb') as f:
        print(f.name)
        up.picture.save(name+'-pic.jpg', File(f))
    u.save()
    up.save()
    return u, up

def add_album(name, artist, cover):
    a = Album.objects.create(name=name, rating=0)
    a.artist=artist
    print('\t' + name)
    ytmusic = YTMusic()
    res = ytmusic.search(artist + ' ' + name)
    for i in range(len(res)):
        if res[i]['resultType'] == "album":
            break
    alb = ytmusic.get_album(res[i]['browseId'])
    songs = alb['tracks']
    for song in list(songs):
        print('\t\t' + song['title'])
    with open('pop-imgs/'+cover, 'rb') as f:
        a.cover.save(name+'-cover.jpg', File(f))
    a.year = alb['year']
    a.rating = 0
    a.save()
    for song in songs:
        Song.objects.create(album=a, name=song['title'], length=song['duration'])
    return a

if __name__ == '__main__':
    print('Starting population')
    clear()
    populate()
    #API.getSongs()#url='https://www.azlyrics.com/lyrics/slipknot/disasterpiece.html')

    #Songs = []
    #for x,each in enumerate(API.songs):
    #    if API.songs[each]['album'] == 'Iowa':
    #        Songs.append(each)

    #print(Songs)


