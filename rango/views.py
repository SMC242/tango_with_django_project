from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


def index(request: HttpRequest) -> HttpResponse:
    context = {"boldmessage": "Crunchy, creamy, cookie, candy, cupcake!"}
    return render(
        request,
        "rango/index.html",
        context=context,
    )


def about(request: HttpRequest) -> HttpResponse:
    context = {"author_name": "Eilidh"}
    return render(request, "rango/about.html", context=context)
