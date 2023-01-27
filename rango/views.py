from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Rango says 'Hey there, partner!'")