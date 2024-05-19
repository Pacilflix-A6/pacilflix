from datetime import datetime, timedelta
import json

from django.http import JsonResponse
from django.shortcuts import render
from django.db import InternalError, connection
from accounts.views import login_required

# Create your views here.

def dictfetchall(cursor):
    "Returns all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def search_tayangan(request):
    cursor = connection.cursor()
    search_query = request.GET.get('q', '')

    # Query untuk mencari film berdasarkan judul
    cursor.execute("""
        SELECT t.id, t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer, 'Film' AS tipe_tayangan
        FROM TAYANGAN AS t
        JOIN FILM AS f ON f.id_tayangan = t.id
        WHERE t.judul ILIKE %s;
    """, [f'%{search_query}%'])
    searched_films = dictfetchall(cursor)

    # Query untuk mencari series berdasarkan judul
    cursor.execute("""
        SELECT t.id, t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer, 'Series' AS tipe_tayangan
        FROM TAYANGAN AS t
        JOIN SERIES AS s ON s.id_tayangan = t.id
        WHERE t.judul ILIKE %s;
    """, [f'%{search_query}%'])
    searched_series = dictfetchall(cursor)

    results = searched_films + searched_series

    username = request.COOKIES.get('username')

    # Query untuk mengambil data status penggguna
    cursor.execute("""
            SELECT CASE 
                WHEN EXISTS (
                    SELECT 1
                    FROM PENGGUNA_AKTIF
                    WHERE username = %s
                ) THEN 'aktif'
                ELSE 'nonaktif'
            END AS status_pembelian_paket;
                    """, [username])
    
    status_pengguna = dictfetchall(cursor)

    return JsonResponse({"results": results, "status_pengguna": status_pengguna})

@login_required
def tayangan(request):
    cursorb = connection.cursor()

    # Query untuk mengambil data film
    cursorb.execute("""
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

    # Query untuk mengambil data tayangan terbaik
    cursorb.execute("""
            WITH RankedTayangan AS (
                SELECT 
                    T.id,
                    T.judul,
                    T.sinopsis_trailer,
                    T.url_video_trailer,
                    T.release_date_trailer,
                    COALESCE(FV.total_view, SV.total_view) AS total_view,
                    CASE
                    WHEN FV.id_tayangan IS NOT NULL THEN 'Film'
                    WHEN SV.id_tayangan IS NOT NULL THEN 'Series'
                    ELSE 'Unknown'
                    END AS tipe_tayangan,
                    ROW_NUMBER() OVER (ORDER BY COALESCE(FV.total_view, SV.total_view) DESC) AS peringkat
                FROM TAYANGAN T
                LEFT JOIN FILM_VIEWERS_LAST_7_DAYS FV ON T.id = FV.id_tayangan
                LEFT JOIN SERIES_VIEWERS_LAST_7_DAYS SV ON T.id = SV.id_tayangan
                )
                SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer, total_view, tipe_tayangan, peringkat
                FROM RankedTayangan
                WHERE peringkat <= 10
                ORDER BY peringkat;
                    """)
    
    best_shows = dictfetchall(cursorb)

    username = request.COOKIES.get('username')

    # Query untuk mengambil data status penggguna
    cursorb.execute("""
            SELECT CASE 
           WHEN EXISTS (
               SELECT 1
               FROM PENGGUNA_AKTIF
               WHERE username = %s
           ) THEN 'aktif'
           ELSE 'nonaktif'
       END AS status_pembelian_paket;
                    """, [username])
    
    status_pengguna = dictfetchall(cursorb)[0]
    print(status_pengguna)

    return render(request, "tayangan.html", {"films": films, "series": series, "best_shows":best_shows, "status_pengguna": status_pengguna})

def trailer(request):
    cursorb = connection.cursor()

    # Query untuk mengambil data film
    cursorb.execute("""
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

    # Query untuk mengambil data tayangan terbaik
    cursorb.execute("""
            WITH RankedTayangan AS (
                SELECT 
                    T.id,
                    T.judul,
                    T.sinopsis_trailer,
                    T.url_video_trailer,
                    T.release_date_trailer,
                    COALESCE(FV.total_view, SV.total_view) AS total_view,
                    CASE
                    WHEN FV.id_tayangan IS NOT NULL THEN 'Film'
                    WHEN SV.id_tayangan IS NOT NULL THEN 'Series'
                    ELSE 'Unknown'
                    END AS tipe_tayangan,
                    ROW_NUMBER() OVER (ORDER BY COALESCE(FV.total_view, SV.total_view) DESC) AS peringkat
                FROM TAYANGAN T
                LEFT JOIN FILM_VIEWERS_LAST_7_DAYS FV ON T.id = FV.id_tayangan
                LEFT JOIN SERIES_VIEWERS_LAST_7_DAYS SV ON T.id = SV.id_tayangan
                )
                SELECT id, judul, sinopsis_trailer, url_video_trailer, release_date_trailer, total_view, tipe_tayangan, peringkat
                FROM RankedTayangan
                WHERE peringkat <= 10
                ORDER BY peringkat;
                    """)
    
    best_shows = dictfetchall(cursorb)

    return render(request, "trailer.html", {"films": films, "series": series, "best_shows": best_shows})

@login_required
def film_select(request, film_id):
    cursorb = connection.cursor()
    cursorb.execute("""
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
            tv.total_view,
            (
                SELECT 
                    json_agg(json_build_object(
                        'username', username,
                        'timestamp', TO_CHAR(timestamp, 'YYYY-MM-DD (HH24:MI:SS)'),
                        'rating', rating,
                        'deskripsi', deskripsi
                    ) ORDER BY timestamp DESC) 
                FROM (
                    SELECT DISTINCT 
                        username, 
                        timestamp, 
                        rating, 
                        deskripsi 
                    FROM ULASAN 
                    WHERE id_tayangan = t.id
                ) AS distinct_ulasan
            ) AS kumpulan_ulasan

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

        WHERE t.id = %s
        GROUP BY t.id, f.id_tayangan, t.judul, t.sinopsis, t.asal_negara, f.url_video_film, f.release_date_film, f.durasi_film, cs.nama, psc.nama, tv.total_view;
        """, [film_id])
    film = dictfetchall(cursorb)[0]

    username = request.COOKIES.get('username')

    cursora = connection.cursor()
    cursora.execute("""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username = %s;
        """, [username]
    )
    favorites = cursora.fetchall()
    
    return render(request, 'film.html', {'film': film, "favorites":favorites})

@login_required
def series_select(request, series_id):
    cursorb = connection.cursor()
    cursorb.execute("""
        SELECT
            s.id_tayangan,
            t.judul AS judul_tayangan,
            t.sinopsis AS sinopsis_tayangan,
            t.asal_negara,
            ROUND(AVG(u.rating), 1) AS rating_rata_rata,
            ARRAY_AGG(DISTINCT gt.genre) AS genre,
            ARRAY_AGG(DISTINCT cpm.nama) AS pemain,
            ARRAY_AGG(DISTINCT psc.nama) AS penulis_skenario,
            cs.nama AS sutradara,
            tv.total_view,
            (
                SELECT 
                    json_agg(json_build_object(
                        'username', username,
                        'timestamp', TO_CHAR(timestamp, 'YYYY-MM-DD (HH24:MI:SS)'),
                        'rating', rating,
                        'deskripsi', deskripsi
                    ) ORDER BY timestamp DESC) 
                FROM (
                    SELECT DISTINCT 
                        username, 
                        timestamp, 
                        rating, 
                        deskripsi 
                    FROM ULASAN 
                    WHERE id_tayangan = t.id
                ) AS distinct_ulasan
            ) AS kumpulan_ulasan,
            (
                SELECT
                    json_agg(json_build_object(
                        'sub_judul', sub_judul,
                        'sinopsis', sinopsis,
                        'durasi', durasi,
                        'url_video', url_video,
                        'release_date', TO_CHAR(release_date, 'YYYY-MM-DD')
                    ) ORDER BY release_date ASC)
                FROM EPISODE
                WHERE id_series = s.id_tayangan
            ) AS kumpulan_episode
        FROM TAYANGAN AS t
        JOIN SERIES AS s ON t.id = s.id_tayangan
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
        LEFT JOIN SERIES_VIEWERS AS tv ON t.id = tv.id_tayangan
        WHERE t.id = %s
        GROUP BY t.id, s.id_tayangan, t.judul, t.sinopsis, t.asal_negara, cs.nama, psc.nama, tv.total_view;
        """, [series_id])
    
    series = dictfetchall(cursorb)[0]

    username = request.COOKIES.get('username')

    cursora = connection.cursor()
    cursora.execute("""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username = %s;
        """, [username]
    )
    favorites = cursora.fetchall()
    
    return render(request, 'series.html', {'series': series, 'favorites': favorites})

@login_required
def episode_select(request, series_id, sub_judul):
    cursorb = connection.cursor()
    cursorb.execute("""
        SELECT
            s.id_tayangan,
            t.judul AS judul_tayangan,
            e.sinopsis AS sinopsis_episode,
            e.sub_judul,
            e.durasi AS durasi_episode,
            e.url_video AS url_episode,
            e.release_date AS tanggal_rilis_episode,
            (
                SELECT
                    json_agg(json_build_object(
                        'sub_judul', sub_judul,
                        'sinopsis', sinopsis,
                        'durasi', durasi,
                        'url_video', url_video,
                        'release_date', TO_CHAR(release_date, 'YYYY-MM-DD')
                    ) ORDER BY release_date ASC)
                FROM EPISODE
                WHERE id_series = s.id_tayangan
            ) AS kumpulan_episode,
            (
                SELECT SUM(durasi)
                FROM EPISODE
                WHERE id_series = s.id_tayangan
            ) AS durasi_series
        FROM TAYANGAN AS t
        JOIN SERIES AS s ON t.id = s.id_tayangan
        LEFT JOIN EPISODE AS e ON s.id_tayangan = e.id_series
        WHERE t.id = %s AND e.sub_judul = %s
        GROUP BY t.id, s.id_tayangan, t.judul, e.sinopsis, e.sub_judul, e.durasi, e.url_video, e.release_date;
        """, [series_id, sub_judul])
    
    episode = dictfetchall(cursorb)[0]
    
    return render(request, 'episode.html', {'episode': episode})

@login_required
def tonton(request, tayangan_id):
    cursor = connection.cursor()

    if request.method == "POST":
        json_data = json.loads(request.body)
        
        # Mendapatkan nilai id_tayangan dan durasi_tonton dari data JSON
        id_tayangan = tayangan_id
        durasi_tonton = json_data.get("durasi_tonton")
        username = request.COOKIES.get('username')
        start_date_time = datetime.now()
        end_date_time = start_date_time + timedelta(minutes=int(durasi_tonton))
        
        cursor.execute("""
            INSERT INTO RIWAYAT_NONTON (id_tayangan, username, start_date_time, end_date_time)
            VALUES (%s, %s, %s, %s);
            """, (id_tayangan, username, start_date_time, end_date_time))
        
        return JsonResponse({"status": "success"})
    
    return JsonResponse({"status": "failed"})

@login_required
def ulas(request, tayangan_id):
    cursor = connection.cursor()

    if request.method == "POST":
        try:
            # Mendapatkan data JSON dari request body
            json_data = json.loads(request.body)
            
            # Mendapatkan nilai id_tayangan dan durasi_tonton dari data JSON
            id_tayangan = tayangan_id
            username = request.COOKIES.get('username')
            timestamp = datetime.now()
            rating = json_data.get("rating")
            deskripsi = json_data.get("deskripsi")

            cursor.execute("""
                INSERT INTO ULASAN (id_tayangan, username, timestamp, rating, deskripsi)
                VALUES (%s, %s, %s, %s, %s);
                """, (id_tayangan, username, timestamp, rating, deskripsi))
            
            return JsonResponse({"status": "success", "message": "Ulasan berhasil dikirim"})
        
        except InternalError as e:
            # Menangkap pesan error dari PostgreSQL
            return JsonResponse({"status": "failed", "error": "Kamu sudah pernah mengulas tayangan ini."})

    return JsonResponse({"status": "failed", "error": "Terjadi kesalahan saat mengirim ulasan."})

