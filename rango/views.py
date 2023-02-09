from django.shortcuts import render
from django.http import HttpResponse, HttpRequest

from rango.models import Category, Page


def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.order_by("-likes")[:5]
    top_pages = Page.objects.order_by("-views")[:5]

    context = {
        "boldmessage": "Crunchy, creamy, cookie, candy, cupcake!",
        "categories": categories,
        "top_pages": top_pages,
    }
    return render(
        request,
        "rango/index.html",
        context=context,
    )


def about(request: HttpRequest) -> HttpResponse:
    context = {"author_name": "Eilidh"}
    return render(request, "rango/about.html", context=context)


def show_category(request: HttpRequest, slug: str) -> HttpResponse:
    try:
        category = Category.objects.get(slug=slug)
        pages = Page.objects.filter(category=category)
        context = {"category": category, "pages": pages}

    except Category.DoesNotExist:
        context = {"category": None, "pages": []}

    return render(request, "rango/category.html", context=context)
