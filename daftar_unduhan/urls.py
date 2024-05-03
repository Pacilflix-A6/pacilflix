from django.urls import path
from daftar_unduhan.views import index

app_name = 'daftar_unduhan'
urlpatterns = [
    path('daftar-unduhan/', index, name='daftar_unduhan_page')
]
