from django.db import models
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver

SMALL_WORDS = ['and', 'the', 'of', 'in', 'on', 'at', 'for', 'to', 'with', 'a', 'an']

def capitalise(title):
    words = title.split()
    for i, word in enumerate(words):
        if i==0 or word.lower() not in SMALL_WORDS:
            words[i] = word.capitalize()
    return ' '.join(words)

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(max_length=256, blank=True)

    def __str__(self):
        return self.user.username

class Album(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=128)
    #genre = models.CharField(max_length=128)
    slug = models.SlugField(unique=True)
    artist = models.CharField(max_length=128)
    year = models.IntegerField(default=0)
    cover = models.ImageField(upload_to='album_covers', blank=True)
    rating = models.DecimalField(max_digits = 3, decimal_places = 2, default=None)

    def save(self, *args, **kwargs):
        self.name = capitalise(self.name)
        #self.artist = capitalise(self.artist)
        self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Song(models.Model):
    id = models.AutoField(primary_key=True)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    #rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)
    length = models.CharField(max_length=5)

    def __str__(self):
        return self.name

class SongRating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)

    class Meta:
        unique_together = ('user', 'song')
