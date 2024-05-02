from django.urls import path
from tayangan.views import tayangan, trailer, film, series, episode

app_name = 'tayangan'

urlpatterns = [
    path('trailer/', trailer, name='trailer'),
    path('', tayangan, name='tayangan'),
    path('film/', film, name='film'),
    path('series/', series, name='series'),
    path('episode/', episode, name='episode'),
]
