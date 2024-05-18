from django.db import connection
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from functools import wraps
from django.urls import reverse

def option(request):
    if request.COOKIES.get('is_authenticated'):
        return HttpResponseRedirect(reverse('tayangan:tayangan'))
    return render(request, "login.html")

def form_login(request):
    return render(request, "form_login.html")

def form_register(request):
    return render(request, "form_register.html")

@csrf_exempt
def login(request):
    context = {"error": ""}
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT username, negara_asal FROM pengguna 
                WHERE username=%s AND password=%s;
                """,(username, password))
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
            context["error"] = "Username atau password salah! Silakan coba lagi."

    return render(request, 'form_login.html', context)

def logout(request):
    response = HttpResponseRedirect(reverse('accounts:login'))
    response.delete_cookie('username')
    response.delete_cookie('negara')
    response.delete_cookie('is_authenticated')
    return response

@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        negara = request.POST.get('negara')
        cursor = connection.cursor()
        try:
            cursor.execute("""
                INSERT INTO PENGGUNA (username, password, negara_asal)
                VALUES (%s, %s, %s)
            """, (username, password, negara))
            return JsonResponse({'status': 'success'})
        except Exception as e:
            print(e)
            return JsonResponse({'status': 'failed'})
        
def login_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.COOKIES.get('is_authenticated'):
            # Jika pengguna tidak terautentikasi, arahkan ke halaman login
            return HttpResponseRedirect(reverse('accounts:form_login'))
        return view_func(request, *args, **kwargs)
    return wrapper