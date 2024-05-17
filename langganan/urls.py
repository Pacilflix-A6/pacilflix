from django.urls import path
from langganan.views import *

app_name = 'langganan'

urlpatterns = [
    path('langganan/', langganan_page, name='langganan_page'),
    path('langganan/beli-langganan', beli_langganan_page, name='beli_langganan_page'),
    path('langganan/proses-transaksi', proses_transaksi, name='proses_transaksi')
]