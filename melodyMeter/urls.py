from django.urls import path
from melodyMeter import views

app_name = 'melodyMeter'

urlpatterns = [
        path('', views.index, name='index'),
        path('albums/', views.albums, name='albums'),
        path('log-in/', views.login, name='login'),
        path('sign-up/', views.signup, name='signup'),
        path('profile/', views.profile, name='profile'),
        path('albums/add-album/', views.add_album, name='add-album'),
        path('albums/<slug:album_name_slug>/', views.show_album, name='show_album'),
]