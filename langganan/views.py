from django.db import connection
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from datetime import datetime, timedelta
from accounts.views import login_required


# Create your views here.
@login_required
def langganan_page(request):
    paket_langganan = get_all_paket()
    riwayat_transaksi = get_riwayat_transaksi(request)
    langganan_aktif = get_langganan_aktif(request)
    return render(request, 'langganan.html', {'paket_langganan':paket_langganan, 'riwayat_transaksi':riwayat_transaksi, 'langganan_aktif':langganan_aktif})

def get_all_paket():
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT p.nama, p.harga, p.resolusi_layar, STRING_AGG(dp.dukungan_perangkat, ', ') AS dukungan_perangkat
        FROM PAKET p
        LEFT JOIN DUKUNGAN_PERANGKAT dp ON p.nama = dp.nama_paket
        GROUP BY p.nama, p.harga, p.resolusi_layar
        ORDER BY p.harga DESC
        """
    )
    paket_langganan = cursor.fetchall()
    return paket_langganan

def get_riwayat_transaksi(request):
    username = request.COOKIES.get('username')
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT t.nama_paket, t.start_date_time, t.end_date_time, t.metode_pembayaran, t.timestamp_pembayaran, p.harga
        FROM TRANSACTION t
        INNER JOIN PAKET p ON t.nama_paket = p.nama
        WHERE t.username = %s
        ORDER BY t.start_date_time DESC
        """,
        [username]
    )
    riwayat_transaksi = cursor.fetchall()
    return riwayat_transaksi

def get_langganan_aktif(request):
    username = request.COOKIES.get('username')
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
        [username]
    )
    langganan_aktif = cursor.fetchall()
    return langganan_aktif

@login_required
def beli_langganan_page(request):
    if request.method == 'POST':
        nama = request.POST.get('nama')
        harga = request.POST.get('harga')
        resolusi = request.POST.get('resolusi')
        dukungan = request.POST.get('dukungan')

        return render(request, 'beli_langganan.html', {'nama': nama, 'harga': harga, 'resolusi': resolusi, 'dukungan': dukungan})
    else:
        return HttpResponseBadRequest("Bad request")

@login_required    
def proses_transaksi(request):
    if request.method == 'POST':
        username = request.COOKIES.get('username')
        nama_paket = request.POST.get('nama')
        metode_pembayaran = request.POST.get('metode_pembayaran')

        start_date_time = datetime.now()
        end_date_time = start_date_time + timedelta(days=30)

        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO TRANSACTION (username, start_date_time, end_date_time, nama_paket, metode_pembayaran, timestamp_pembayaran)
            VALUES (%s, %s, %s, %s, %s, CURRENT_TIMESTAMP)
            """,
            [username, start_date_time, end_date_time, nama_paket, metode_pembayaran]
        )

        return redirect('langganan:langganan_page')
    else:
        return HttpResponseBadRequest("Bad request")
    
    
