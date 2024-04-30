from django.urls import path
from daftar_kontributor.views import *

app_name = 'daftar_kontributor'

urlpatterns = [
    path('daftar_kontributor/', daftar_kontributor_page, name='daftar_kontributor_page')
]