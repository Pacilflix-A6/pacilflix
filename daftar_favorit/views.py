from django.shortcuts import render, redirect
from django.db import connection
from accounts.sharedpref import *

def index(request):
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username = '{LoggedInUser.username}';
        """
    )
    
    return render(request, 'daftar_favorit.html', {'favorites': cursor.fetchall()})

def detail_fav(request, timestamp, judul_daftar_fav):
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT a.judul
        FROM TAYANGAN AS a
        JOIN TAYANGAN_MEMILIKI_DAFTAR_FAVORIT AS b ON a.id = b.id_tayangan
        WHERE b.username = '{LoggedInUser.username}' AND b.timestamp = '{timestamp}';
        """
    )
    
    return render(request, 'detail_daftar_favorit.html', {'movies': cursor.fetchall(), 'judul_daftar_fav':judul_daftar_fav})

def delete_daftar_fav(request, timestamp):
    cursor = connection.cursor()
    cursor.execute(f"""
        DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT 
        WHERE username = '{LoggedInUser.username}' 
        AND timestamp = '{timestamp}';

        DELETE FROM DAFTAR_FAVORIT WHERE username = '{LoggedInUser.username}' AND timestamp = '{timestamp}';
        """
    )
    
    return redirect('daftar_favorit:daftar_favorit_page')

def delete_fav(request, judul):
    cursor = connection.cursor()
    cursor.execute(f"""
        DELETE FROM TAYANGAN_MEMILIKI_DAFTAR_FAVORIT 
        WHERE username = '{LoggedInUser.username}' 
        AND id_tayangan = (
            SELECT id 
            FROM TAYANGAN 
            WHERE judul = '{judul}'
        );
        """
    )
    
    return redirect('daftar_favorit:daftar_favorit_page')

def add_fav(request, judul_fav, judul_daftar):
    cursor = connection.cursor()
    cursor.execute(f"""
        INSERT INTO TAYANGAN_MEMILIKI_DAFTAR_FAVORIT(id_tayangan, timestamp, username)
        SELECT b.id, a.timestamp, a.username
        FROM DAFTAR_FAVORIT a
        JOIN TAYANGAN b ON b.judul = '{judul_fav}'
        WHERE a.username = '{LoggedInUser.username}' AND timestamp = (
            SELECT timestamp 
            FROM DAFTAR_FAVORIT 
            WHERE judul = '{judul_daftar}'
        );
        """
    )
    return render(request, "tayangan.html")


