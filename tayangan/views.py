from django.shortcuts import render
from django.db import connection

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
        SELECT t.judul, t.sinopsis, t.url_video_trailer, f.release_date_film
        FROM FILM AS f
        JOIN TAYANGAN AS t ON f.id_tayangan = t.id;
        """)
    films = dictfetchall(cursorb)
    
    # Query untuk mengambil data series
    cursorb.execute("""
        SELECT t.judul, t.sinopsis, t.url_video_trailer, t.release_date_trailer
        FROM SERIES AS s
        JOIN TAYANGAN AS t ON s.id_tayangan = t.id;
    """)
    series = dictfetchall(cursorb)

    return render(request, "tayangan.html", {"films": films, "series": series})

def trailer(request):
    cursorb = connection.cursor()

    # Query untuk mengambil data film
    cursorb.execute(f"""
        SELECT t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer
        FROM FILM AS f
        JOIN TAYANGAN AS t ON f.id_tayangan = t.id;
        """)
    films = dictfetchall(cursorb)
    
    # Query untuk mengambil data series
    cursorb.execute("""
        SELECT t.judul, t.sinopsis_trailer, t.url_video_trailer, t.release_date_trailer
        FROM SERIES AS s
        JOIN TAYANGAN AS t ON s.id_tayangan = t.id;
    """)
    series = dictfetchall(cursorb)

    return render(request, "trailer.html", {"films": films, "series": series})

def film(request):

    # ini buat dropdown daftar favorit di modal favorit
    cursorb = connection.cursor()
    cursorb.execute(f"""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username = 'john_doe';
        """
    )

    context = {
        # bisa tambahin disini aja buat output query lu
        'favorites': cursorb.fetchall()
    }
    return render(request, "film.html", context)

def series(request):

    # ini buat dropdown daftar favorit di modal favorit
    cursorb = connection.cursor()
    cursorb.execute(f"""
        SELECT judul, timestamp
        FROM DAFTAR_FAVORIT
        WHERE username = 'john_doe';
        """
    )

    context = {
        # bisa tambahin disini aja buat output query lu
        'favorites': cursorb.fetchall()
    }
    return render(request, "series.html", context)

def episode(request):
    return render(request, "episode.html")


