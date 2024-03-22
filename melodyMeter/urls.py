from django.urls import path
from melodyMeter import views

app_name = 'melodyMeter'

urlpatterns = [
        path('', views.index, name='index'),
        path('albums/', views.albums, name='albums'),
        path('log-in/', views.login, name='login'),
        path('logout', views.logout, name='logout'),
        path('sign-up/', views.signup, name='signup'),
        path('profile/', views.profile, name='profile'),
        path('edit_profile/', views.edit_profile, name='edit_profile'),
        path('albums/<slug:album_name_slug>/rate-song/<int:song_id>', views.rate_song, name='rate-song'),
        path('get-alert-contents/', views.get_alert_contents, name='get_alert_contents'),
        path('albums/add-album/', views.add_album, name='add-album'),
        path('albums/<slug:album_name_slug>/', views.show_album, name='show_album'),
]
