from django.shortcuts import render

# Create your views here.
def langganan_page(request):
    return render(request, 'langganan.html')

def beli_langganan_page(request):
    return render(request, 'beli_langganan.html')