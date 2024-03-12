import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'WADProject.settings')

import django
django.setup()
from melodyMeter.models import Album, Song

import azapi

def populate():
    iowa_songs=[
            {
                "name": "Disasterpiece",
                "rating": 5
             },
            {
                "name": "People = Shit",
                "rating": 5
            },
            {
                "name": "The Heretic Anthem",
                "rating": 5
            }
            ]

    albums = {
            "Iowa": {"songs": iowa_songs, "genre":"nu-metal", "year":2001}
    }#,
        #{
         #   "name":"If I Can't Have Love I Want Power",
          #  "genre":"Pop",
           # "songs":halsey_songs
        #}

    for album, albumdata in albums.items():
        a = add_album(album, albumdata['genre'], albumdata['year'])
        for s in albumdata['songs']:
            add_song(a,s['name'], s['rating'])

    for a in Album.objects.all():
        for s in Song.objects.filter(album=a):
            print(f'- {a}: {s}')

def add_song(album, name, rating):
    s = Song.objects.get_or_create(album=album, name=name)[0]
    s.rating=rating
    s.save()

def add_album(name, genre, year):
    a = Album.objects.get_or_create(name=name)[0]
    a.genre=genre
    a.year=year
    a.save()
    return a

if __name__ == '__main__':
    print('Starting population')
    populate()
    #API = azapi.AZlyrics()

    #API.artist = 'Slipknot'

    #API.getSongs()#url='https://www.azlyrics.com/lyrics/slipknot/disasterpiece.html')

    #Songs = []
    #for x,each in enumerate(API.songs):
    #    if API.songs[each]['album'] == 'Iowa':
    #        Songs.append(each)

    #print(Songs)


