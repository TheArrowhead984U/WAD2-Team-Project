from django import forms
from django.contrib.auth.models import User
from melodyMeter.models import Album, Song, UserProfile

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('picture',)

class AlbumForm(forms.ModelForm):
    name = forms.CharField(max_length=128, help_text="Please enter the album name.", label="Album Name")
    artist = forms.CharField(max_length=128, help_text="Please enter the artist's name.", label="Album Artist")
    slug = forms.CharField(widget=forms.HiddenInput(), initial=0)
    year = forms.IntegerField()

    class Meta:
        model = Album
        fields = ('name','artist','year')
