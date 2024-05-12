from django.urls import path
from daftar_favorit.views import *

app_name = 'daftar_favorit'
urlpatterns = [
    path('daftar-favorit/', index, name='daftar_favorit_page'),
    path('detail_daftar-favorit/<str:timestamp>/<str:judul_daftar_fav>/', detail_fav, name='detail_daftar_favorit_page'),
    path('del-daftar-favorit/<str:timestamp>/', delete_daftar_fav, name='delete_daftar_favorit'),
    path('del-favorit/<str:judul>/', delete_fav, name='delete_favorit'),
    path('add-favorit/<str:judul_fav>/<str:judul_daftar>/', add_fav, name='add_favorit'),
]
