from django.shortcuts import render
from django.db import connection

# Create your views here.
def tayangan(request):
    return render(request, "tayangan.html")

def trailer(request):
    return render(request, "trailer.html")

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


