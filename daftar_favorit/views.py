from django.shortcuts import render, redirect
from django.db import connection
from accounts.views import login_required

@login_required
def index(request):
    username = request.COOKIES.get('username')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username =%s;
        """, (username,)
    )
    
    return render(request, 'daftar_favorit.html', {'favorites': cursor.fetchall()})

@login_required
def detail_fav(request, timestamp, judul_daftar_fav):
    username = request.COOKIES.get('username')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.judul
        FROM TAYANGAN AS a
        JOIN TAYANGAN_MEMILIKI_DAFTAR_FAVORIT AS b ON a.id = b.id_tayangan
        WHERE b.username =%s AND b.timestamp =%s;
        """, (username, timestamp)
    )
    
    return render(request, 'detail_daftar_favorit.html', {'movies': cursor.fetchall(), 'judul_daftar_fav':judul_daftar_fav})

@login_required
def delete_daftar_fav(request, timestamp):
    username = request.COOKIES.get('username')
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT 
        WHERE username = %s 
        AND timestamp = %s;

        DELETE FROM DAFTAR_FAVORIT WHERE username =%s AND timestamp =%s;
        """, (username, timestamp, username, timestamp)
    )
    
    return redirect('daftar_favorit:daftar_favorit_page')

@login_required
def delete_fav(request, judul):
    username = request.COOKIES.get('username')
    cursor = connection.cursor()
    cursor.execute("""
        DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT 
        WHERE username =%s 
        AND id_tayangan = (
            SELECT id 
            FROM TAYANGAN 
            WHERE judul =%s
        );
        """, (username, judul)
    )
    
    return redirect('daftar_favorit:daftar_favorit_page')

@login_required
def add_fav(request, judul_fav, judul_daftar):
    username = request.COOKIES.get('username')
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO TAYANGAN_MEMILIKI_DAFTAR_FAVORIT(id_tayangan, timestamp, username)
        SELECT b.id, a.timestamp, a.username
        FROM DAFTAR_FAVORIT a
        JOIN TAYANGAN b ON b.judul =%s
        WHERE a.username = %s AND timestamp = (
            SELECT timestamp 
            FROM DAFTAR_FAVORIT 
            WHERE judul = %s
        );
        """, (judul_fav, username, judul_daftar)
    )
    return render(request, "tayangan.html")


