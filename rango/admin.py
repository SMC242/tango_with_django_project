from django.contrib import admin
from django.db.models import Model

from rango.models import Category, Page


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url")


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}


# Register your models here.
models: list[Model | admin.ModelAdmin] = []

for m in models:
    admin.site.register(m)
