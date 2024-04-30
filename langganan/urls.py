from django.urls import path
from langganan.views import *

app_name = 'langganan'

urlpatterns = [
    path('langganan/', langganan_page, name='langganan_page')
]