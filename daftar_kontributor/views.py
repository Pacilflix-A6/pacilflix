from django.shortcuts import render
from django.db import connection

def daftar_kontributor_page(request):
    contributors = get_all_contributors()
    return render(request, 'daftar_kontributor.html', {'contributors': contributors})

def get_all_contributors():
    cursor = connection.cursor()
    cursor.execute(
        """
        SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan,
            CASE
                WHEN ps.id IS NOT NULL THEN 'Penulis Skenario'
                WHEN pm.id IS NOT NULL THEN 'Pemain'
                WHEN st.id IS NOT NULL THEN 'Sutradara'
                ELSE 'Unknown'
            END AS tipe
        FROM CONTRIBUTORS c
        LEFT JOIN PENULIS_SKENARIO ps ON c.id = ps.id
        LEFT JOIN PEMAIN pm ON c.id = pm.id
        LEFT JOIN SUTRADARA st ON c.id = st.id
        """
    )
    
    contributors = cursor.fetchall()
    return contributors