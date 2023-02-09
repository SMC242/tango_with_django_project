from django.urls import path

from rango import views

app_name = "rango"

urlpatterns = [
    path("", views.index, name="index"),
    path("about", views.about, name="about"),
    path("category/<slug:slug>/", views.show_category, name="show_category"),
]
