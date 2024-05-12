from django.urls import path
from daftar_unduhan.views import *

app_name = 'daftar_unduhan'
urlpatterns = [
    path('daftar-unduhan/', index, name='daftar_unduhan_page'),
    path('delete-download/<str:judul>/', delete_download, name='delete_download'),
    path('add-download/<str:judul>/', add_download, name='add_download')
]
