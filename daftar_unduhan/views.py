from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection
from django.urls import reverse
from accounts.views import login_required

@login_required
def index(request):
    username = request.COOKIES.get('username')
    cursor = connection.cursor()
    cursor.execute("""
        SELECT a.judul, b.timestamp
        FROM TAYANGAN_TERUNDUH AS b
        JOIN TAYANGAN AS a ON b.id_tayangan = a.id
        WHERE username =%s;
        """, (username,)
    )
    return render(request, 'daftar_unduhan.html', {'downloads': cursor.fetchall()})

@login_required
def delete_download(request, judul):
    if request.method == "DELETE":
        username = request.COOKIES.get('username')
        cursor = connection.cursor()
        cursor.execute("""
            DELETE FROM TAYANGAN_TERUNDUH WHERE username =%s AND id_tayangan = (
            SELECT id 
            FROM TAYANGAN 
            WHERE judul =%s
            );
            """, (username, judul)
        )

        if cursor.rowcount == 0:
            return JsonResponse({'status': 'failed'})
        else:
            return JsonResponse({'status': 'success', 'redirect_url': reverse('daftar_unduhan:daftar_unduhan_page')})

@login_required        
def add_download(request, judul):
    username = request.COOKIES.get('username')
    cursor = connection.cursor()
    cursor.execute("""
        SET TIME ZONE 'Asia/Jakarta';
        INSERT INTO TAYANGAN_TERUNDUH (id_tayangan, username, timestamp)
        SELECT id, %s , CURRENT_TIMESTAMP
        FROM TAYANGAN AS a
        WHERE judul = %s;
        """, (username, judul)
    )

    return JsonResponse({'status': 'success'})
