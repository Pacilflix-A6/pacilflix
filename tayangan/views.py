from django.shortcuts import render

# Create your views here.
def tayangan(request):
    return render(request, "tayangan.html")

def trailer(request):
    return render(request, "trailer.html")

def film(request):
    return render(request, "film.html")

def series(request):
    return render(request, "series.html")

def episode(request):
    return render(request, "episode.html")


