from django.http import HttpResponse
from django.shortcuts import render


def index(request):
    return render(request, 'kelp/index.html')

def populate_db(request):
    pass
    return HttpResponse("everything is cool")

