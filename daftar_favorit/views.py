from django.shortcuts import render

def index(request):
    return render(request, 'daftar_favorit.html')