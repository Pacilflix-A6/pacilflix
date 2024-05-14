from django.db import connection
from django.shortcuts import render
from accounts.sharedpref import *

# Create your views here.
def langganan_page(request):
    paket_langganan = get_all_paket()
    riwayat_transaksi = get_riwayat_transaksi()
    langganan_aktif = get_langganan_aktif()
    return render(request, 'langganan.html', {'paket_langganan':paket_langganan, 'riwayat_transaksi':riwayat_transaksi, 'langganan_aktif':langganan_aktif})

def get_all_paket():
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT p.nama, p.harga, p.resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ', ') AS dukungan_perangkat
        FROM PAKET p
        LEFT JOIN DUKUNGAN_PERANGKAT dp ON p.nama = dp.nama_paket
        GROUP BY p.nama, p.harga, p.resolusi_layar
        """
    )
    paket_langganan = cursor.fetchall()
    return paket_langganan

def get_riwayat_transaksi():
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT t.nama_paket, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran, p.harga
        FROM TRANSACTION t
        INNER JOIN PAKET p ON t.nama_paket = p.nama
        WHERE t.username = %s
        """,
        [LoggedInUser.username]
    )
    riwayat_transaksi = cursor.fetchall()
    return riwayat_transaksi

def get_langganan_aktif():
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT t.nama_paket, p.harga, p.resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ', ') AS dukungan_perangkat, t.start_date_time, t.end_date_time
        FROM TRANSACTION t
        INNER JOIN PAKET p ON t.nama_paket = p.nama
        LEFT JOIN DUKUNGAN_PERANGKAT dp ON p.nama = dp.nama_paket
        WHERE t.username = %s
        AND t.end_date_time > CURRENT_TIMESTAMP
        GROUP BY t.nama_paket, p.harga, p.resolusi_layar, t.start_date_time, t.end_date_time;
        """,
        [LoggedInUser.username]
    )
    langganan_aktif = cursor.fetchall()
    return langganan_aktif

def beli_langganan_page(request):
    return render(request, 'beli_langganan.html')