from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from rango.models import Category, Page
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm


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
            return redirect(reverse("rango:index"))
        else:
            print(form.errors)

    return render(request, "rango/add_category.html", {"form": form})


def add_page(request: HttpRequest, category_name_slug: str) -> HttpResponse:
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        return redirect(reverse("rango:index"))

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


def register(request: HttpRequest) -> HttpResponse:
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)

    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(
        request,
        "rango/register.html",
        context={
            "user_form": user_form,
            "profile_form": profile_form,
            "registered": registered,
        },
    )


def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("rango:index"))
            else:
                return HttpResponse("Your Ranog account is disabled.")

        else:
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")

    else:
        return render(request, "rango/login.html")


@login_required
def restricted(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Since you're logged in, you can see this text!")


@login_required
def user_logout(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect(reverse("rango:index"))
