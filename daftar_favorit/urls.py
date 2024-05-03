from django.urls import path
from daftar_favorit.views import index

app_name = 'daftar_favorit'
urlpatterns = [
    path('daftar-favorit/', index, name='daftar_favorit_page')
]
