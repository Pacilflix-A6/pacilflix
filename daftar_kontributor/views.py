from django.shortcuts import render
from django.db import connection
from accounts.views import login_required

@login_required
def daftar_kontributor_page(request):
    if request.method == 'POST':
        contributor_type = request.POST.get('contributorType')
        if contributor_type == 'all':
            contributors = get_all_contributors()
        else:
            contributors = filter_contributors_by_type(contributor_type)
    else:
        contributors = get_all_contributors()
        contributor_type = request.GET.get('contributorType', 'all')
    return render(request, 'daftar_kontributor.html', {'contributors': contributors, 'selected_type': contributor_type})

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

def filter_contributors_by_type(contributor_type):
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
        HAVING STRING_AGG(type_name, ', ') LIKE %s
        """,
        ["%" + contributor_type + "%"]
    )
    
    contributors = cursor.fetchall()
    return contributors
