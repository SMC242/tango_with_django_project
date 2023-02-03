from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "Rango says 'Hey there, partner!'<br/><a href='/rango/about'>About page</a>"
    )


def about(request: HttpRequest) -> HttpResponse:
    return HttpResponse(
        "Rango says 'Here is the about page.'<br/><a href='/rango/'>Rango home page</a>"
    )
