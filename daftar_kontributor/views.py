from django.shortcuts import render

# Create your views here.
def daftar_kontributor_page(request):
    return render(request, 'index.html')