from django.urls import path
from tayangan.views import tayangan, trailer, film, series, episode, film_select, tonton, ulas

app_name = 'tayangan'

urlpatterns = [
    path('trailer/', trailer, name='trailer'),
    path('', tayangan, name='tayangan'),
    path('film/<uuid:film_id>/', film_select, name='film_select'),
    path('film/', film, name='film'),
    path('series/', series, name='series'),
    path('episode/', episode, name='episode'),
    path('film/<uuid:film_id>/tonton/', tonton, name='tonton'),
    path('film/<uuid:film_id>/ulas/', ulas, name='ulas')
    # path('film/<uuid:film_id>/', film_detail, name='film_detail'),
]
