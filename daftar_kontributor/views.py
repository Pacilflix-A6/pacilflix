from django.shortcuts import render
from django.db import connection

def daftar_kontributor_page(request):
    contributors = get_all_contributors()
    return render(request, 'daftar_kontributor.html', {'contributors': contributors})

def get_all_contributors():
    cursor = connection.cursor()
    cursor.execute(
         """
        SELECT contributors.id, contributors.nama, contributors.jenis_kelamin, contributors.kewarganegaraan,
            STRING_AGG(type_name, ', ') AS tipe
        FROM (
            SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan,
                CASE WHEN ps.id IS NOT NULL THEN 'Penulis Skenario' ELSE NULL END AS type_name
                FROM CONTRIBUTORS c
                LEFT JOIN PENULIS_SKENARIO ps ON c.id = ps.id
            UNION ALL
            SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan,
                CASE WHEN pm.id IS NOT NULL THEN 'Pemain' ELSE NULL END AS type_name
                FROM CONTRIBUTORS c
                LEFT JOIN PEMAIN pm ON c.id = pm.id
            UNION ALL
            SELECT c.id, c.nama, c.jenis_kelamin, c.kewarganegaraan,
                CASE WHEN st.id IS NOT NULL THEN 'Sutradara' ELSE NULL END AS type_name
                FROM CONTRIBUTORS c
                LEFT JOIN SUTRADARA st ON c.id = st.id
        ) AS types
        LEFT JOIN CONTRIBUTORS ON types.id = contributors.id
        GROUP BY contributors.id, contributors.nama, contributors.jenis_kelamin, contributors.kewarganegaraan
        """
    )
    
    contributors = cursor.fetchall()
    return contributors