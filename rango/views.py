from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.urls import reverse

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm


def index(request: HttpRequest) -> HttpResponse:
    categories = Category.objects.order_by("-likes")[:5]
    pages = Page.objects.order_by("-views")[:5]

    context = {
        "boldmessage": "Crunchy, creamy, cookie, candy, cupcake!",
        "categories": categories,
        "pages": pages,
    }
    return render(
        request,
        "rango/index.html",
        context=context,
    )


def about(request: HttpRequest) -> HttpResponse:
    context = {"author_name": "Eilidh"}
    return render(request, "rango/about.html", context=context)


def show_category(request: HttpRequest, category_name_slug: str) -> HttpResponse:
    try:
        category = Category.objects.get(slug=category_name_slug)
        pages = Page.objects.filter(category=category)
        context = {"category": category, "pages": pages}

    except Category.DoesNotExist:
        context = {"category": None, "pages": None}

    return render(request, "rango/category.html", context=context)


def add_category(request: HttpRequest) -> HttpResponse:
    form = CategoryForm()

    if request.method == "POST":
        form = CategoryForm(request.POST)

        if form.is_valid():
            form.save(commit=True)
            return redirect("/rango/")
        else:
            print(form.errors)

    return render(request, "rango/add_category.html", {"form": form})


def add_page(request: HttpRequest, category_name_slug: str) -> HttpResponse:
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect("/rango/")

    form = PageForm()
    if request.method == "POST":
        form = PageForm(request.POST)

        if form.is_valid():
            page = form.save(commit=False)
            page.category = category
            page.views = 0
            page.save()
            return redirect(
                reverse(
                    "rango:show_category",
                    kwargs={"category_name_slug": category_name_slug},
                )
            )
        else:
            print(form.errors)

    context = {"form": form, "category": category}
    return render(request, "rango/add_page.html", context=context)
