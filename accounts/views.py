from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request, "login.html")

def form_login(request):
    return render(request, "form_login.html")

def form_register(request):
    return render(request, "form_register.html")