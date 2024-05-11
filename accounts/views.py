from django.db import connection
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

def option(request):
    return render(request, "login.html")

def form_login(request):
    return render(request, "form_login.html")

def form_register(request):
    return render(request, "form_register.html")

def login(request):
    context = {"error": ""}
    if request.method == "POST":
        nama = request.POST.get("username")
        password = request.POST.get("password")
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT username, negara_asal FROM pengguna WHERE username='{nama}' AND password='{password}';")
            result = cursor.fetchall()
        
        if len(result) != 0:
            username = result[0][0]
            negara = result[0][1]
            response = HttpResponseRedirect(reverse("tayangan:tayangan"))
            
            response.set_cookie('username', username)
            response.set_cookie('negara', negara)
            response.set_cookie('is_authenticated', "True")
            
            return response
        else:
            context = {"is_error": True}

    return render(request, 'login.html', context)

def logout(request):
    response = HttpResponseRedirect(reverse('accounts:login'))
    response.delete_cookie('username')
    response.delete_cookie('negara')
    response.delete_cookie('is_authenticated')
    return response