from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from django.urls import reverse
from accounts.sharedpref import *

def index(request):
    cursor = connection.cursor()
    cursor.execute(f"""
        SELECT a.judul, b.timestamp
        FROM TAYANGAN_TERUNDUH AS b
        JOIN TAYANGAN AS a ON b.id_tayangan = a.id
        WHERE username = '{LoggedInUser.username}';
        """
    )
    return render(request, 'daftar_unduhan.html', {'downloads': cursor.fetchall()})

def delete_download(request, judul):
    if request.method == "DELETE":
        cursor = connection.cursor()
        cursor.execute(f"""
            DELETE FROM TAYANGAN_TERUNDUH WHERE username = '{LoggedInUser.username}' AND id_tayangan = (
            SELECT id 
            FROM TAYANGAN 
            WHERE judul = '{judul}'
            );
            """
        )

        if cursor.rowcount == 0:
            return JsonResponse({'status': 'failed'})
        else:
            return JsonResponse({'status': 'success', 'redirect_url': reverse('daftar_unduhan:daftar_unduhan_page')})
        
def add_download(request, judul):
    cursor = connection.cursor()
    cursor.execute(f"""
        SET TIME ZONE 'Asia/Jakarta';
        INSERT INTO TAYANGAN_TERUNDUH (id_tayangan, username, timestamp)
        SELECT id, '{LoggedInUser.username}', CURRENT_TIMESTAMP
        FROM TAYANGAN AS a
        WHERE judul = '{judul}';
        """
    )

    return JsonResponse({'status': 'success'})
