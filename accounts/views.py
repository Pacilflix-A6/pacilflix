from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
def option(request):
    return render(request, "login.html")

def form_login(request):
    return render(request, "form_login.html")

def form_register(request):
    return render(request, "form_register.html")

#Hafiz make
def login(request):
    print("hai")
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT * from pengguna")
        result = cursor.fetchall()
        print(result)
    context = {"error": ""}
    if request.method == "POST":
        # GET DATA
        nama = request.POST.get("username")
        password = request.POST.get("password")
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT username, negara_asal FROM pengguna WHERE username='{nama}' AND password='{password}';")
            result = cursor.fetchall()
        print(result)
        
        if len(result) != 0:
            username = result[0][0]
            negara = result[0][1]
            response = HttpResponseRedirect(reverse("tayangan:tayangan"))
            
            # SET COOKIES
            response.set_cookie('username', username)
            response.set_cookie('negara', negara)
            response.set_cookie('is_authenticated', "True")
            
            # REDIRECT
            return response
        else:
            context = {"is_error": True}

    return render(request, 'login.html', context)

def logout(request):
    # DELETE COOKIES
    response = HttpResponseRedirect(reverse('accounts:login'))
    response.delete_cookie('username')
    response.delete_cookie('negara')
    response.delete_cookie('is_authenticated')
    return response