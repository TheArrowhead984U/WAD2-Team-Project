from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)

    bio = models.TextField(max_length=500, blank=True)

    def __str__(self):
        return self.user.username

class Album(models.Model):
    name = models.CharField(max_length=128)
    genre = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Album, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Song(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    name = models.CharField(max_length=128)
    rating = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(5)], null=True)

    def __str__(self):
        return self.name
