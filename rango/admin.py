from django.contrib import admin

from rango.models import Category, Page

# Register your models here.
models = [
    Category,
    Page
]

for m in models:
    admin.site.register(m)