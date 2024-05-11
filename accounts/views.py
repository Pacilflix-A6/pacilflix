from django.shortcuts import render
from django.db import connection

# Create your views here.
def login(request):
    cursora = connection.cursor()
    cursora.execute("""SELECT * FROM PAKET;""")
    print(cursora.fetchall())
    return render(request, "login.html")

def form_login(request):
    return render(request, "form_login.html")

def form_register(request):
    return render(request, "form_register.html")