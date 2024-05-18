from django.urls import path
from tayangan.views import tayangan, trailer, film, series, episode, film_select, tonton, series_select, ulas, episode_select

app_name = 'tayangan'

urlpatterns = [
    path('trailer/', trailer, name='trailer'),
    path('', tayangan, name='tayangan'),
    path('film/<uuid:film_id>/', film_select, name='film_select'),
    path('film/', film, name='film'),
    path('series/<uuid:series_id>/', series_select, name='series_select'),
    path('series/<uuid:series_id>/<str:sub_judul>/', episode_select, name='episode_select'),
    path('series/', series, name='series'),
    path('episode/', episode, name='episode'),
    path('<uuid:tayangan_id>/tonton/', tonton, name='tonton'),
    path('<uuid:tayangan_id>/ulas/', ulas, name='ulas')
]
