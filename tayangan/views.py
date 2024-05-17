from datetime import datetime, timedelta
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.db import connection

from accounts.sharedpref import LoggedInUser

# Create your views here.

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def tayangan(request):
    cursorb = connection.cursor()

    # Query untuk mengambil data film
    cursorb.execute(f"""
        SELECT t.judul, t.sinopsis, t.url_video_trailer, f.release_date_film, t.id
        FROM FILM AS f
        JOIN TAYANGAN AS t ON f.id_tayangan = t.id;
        """)
    films = dictfetchall(cursorb)
    
    # Query untuk mengambil data series
    cursorb.execute("""
        SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer, t.id
        FROM SERIES AS s
        JOIN TAYANGAN AS t ON s.id_tayangan = t.id;
    """)
    series = dictfetchall(cursorb)

    return render(request, "tayangan.html", {"films": films, "series": series})

def trailer(request):
    cursorb = connection.cursor()

    # Query untuk mengambil data film
    cursorb.execute(f"""
        SELECT t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer, t.id
        FROM FILM AS f
        JOIN TAYANGAN AS t ON f.id_tayangan = t.id;
        """)
    films = dictfetchall(cursorb)
    
    # Query untuk mengambil data series
    cursorb.execute("""
        SELECT t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer, t.id
        FROM SERIES AS s
        JOIN TAYANGAN AS t ON s.id_tayangan = t.id;
    """)
    series = dictfetchall(cursorb)

    return render(request, "trailer.html", {"films": films, "series": series})

def film_select(request, film_id):
    cursorb = connection.cursor()
    cursorb.execute(f"""
        SELECT 
            f.id_tayangan,
            t.judul AS judul_tayangan, 
            t.sinopsis AS sinopsis_tayangan,
            t.asal_negara,
            f.url_video_film, 
            f.release_date_film,
            f.durasi_film,
            ROUND(AVG(u.rating), 1) AS rating_rata_rata,
            ARRAY_AGG(DISTINCT gt.genre) AS genre,
            ARRAY_AGG(DISTINCT cpm.nama) AS pemain,
            ARRAY_AGG(DISTINCT psc.nama) AS penulis_skenario,
            cs.nama AS sutradara,
            tv.total_view
        FROM TAYANGAN AS t
        JOIN FILM AS f ON t.id = f.id_tayangan
        LEFT JOIN ULASAN AS u ON t.id = u.id_tayangan
        LEFT JOIN GENRE_TAYANGAN as gt ON t.id = gt.id_tayangan
        LEFT JOIN MENULIS_SKENARIO_TAYANGAN AS mst ON t.id = mst.id_tayangan
        LEFT JOIN PENULIS_SKENARIO AS ps ON mst.id_penulis_skenario = ps.id
        LEFT JOIN CONTRIBUTORS AS psc ON ps.id = psc.id
        LEFT JOIN SUTRADARA AS p ON t.id_sutradara = p.id
        LEFT JOIN CONTRIBUTORS AS cs ON p.id = cs.id
        LEFT JOIN MEMAINKAN_TAYANGAN AS mt ON t.id = mt.id_tayangan
        LEFT JOIN PEMAIN AS pm ON mt.id_pemain = pm.id
        LEFT JOIN CONTRIBUTORS AS cpm ON pm.id = cpm.id
        LEFT JOIN FILM_VIEWERS AS tv ON t.id = tv.id_tayangan

        WHERE t.id = '{film_id}'
        GROUP BY f.id_tayangan, t.judul, t.sinopsis, t.asal_negara, f.url_video_film, f.release_date_film, f.durasi_film, cs.nama, psc.nama, tv.total_view;
        """)
    film = dictfetchall(cursorb)[0]

    # print(film)
    
    return render(request, 'film.html', {'film': film})

def tonton(request, film_id):
    cursor = connection.cursor()

    if request.method == "POST":
        # id_tayangan = request.body[0]
        # print(request.body)
        # print(id_tayangan)
        # Mendapatkan data JSON dari request body
        json_data = json.loads(request.body)
        
        # Mendapatkan nilai id_tayangan dan durasi_tonton dari data JSON
        id_tayangan = json_data.get("id_tayangan")
        durasi_tonton = json_data.get("durasi_tonton")
        username = LoggedInUser.username
        start_date_time = datetime.now()
        end_date_time = start_date_time + timedelta(minutes=int(durasi_tonton))
        
        cursor.execute(f"""
            INSERT INTO RIWAYAT_NONTON (id_tayangan, username, start_date_time, end_date_time)
            VALUES (%s, %s, %s, %s);
            """, (id_tayangan, username, start_date_time, end_date_time))
        

        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "failed"})

def ulas(request, film_id):
    cursor = connection.cursor()

    if request.method == "POST":
        # id_tayangan = request.body[0]
        # print(request.body)
        # print(id_tayangan)
        # Mendapatkan data JSON dari request body
        json_data = json.loads(request.body)
        
        # Mendapatkan nilai id_tayangan dan durasi_tonton dari data JSON
        id_tayangan = film_id
        username = LoggedInUser.username
        timestamp = datetime.now()
        rating = json_data.get("rating")
        deskripsi = json_data.get("deskripsi")

        cursor.execute(f"""
            NSERT INTO ULASAN (id_tayangan, username, timestamp, rating, deskripsi)
            VALUES (%s, %s, %s, %s, %s);
            """, (id_tayangan, username, timestamp, rating, deskripsi))
        

        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "failed"})

def film(request):

    # ini buat dropdown daftar favorit di modal favorit
    cursorb = connection.cursor()
    cursorb.execute("""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username = %s;
        """, [LoggedInUser.username]
    )

    context = {
        # bisa tambahin disini aja buat output query lu
        'favorites': cursorb.fetchall()
    }
    return render(request, "film.html", context)

def series(request):

    # ini buat dropdown daftar favorit di modal favorit
    cursorb = connection.cursor()
    cursorb.execute("""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username = %s;
        """, [LoggedInUser.username]
    )

    context = {
        # bisa tambahin disini aja buat output query lu
        'favorites': cursorb.fetchall()
    }
    return render(request, "series.html", context)

def episode(request):
    return render(request, "episode.html")


