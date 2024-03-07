from django.contrib import admin
from melodyMeter.models import Album, Song, UserProfile

class AlbumAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

# Register your models here.
admin.site.register(Album, AlbumAdmin)
admin.site.register(Song)
admin.site.register(UserProfile)
