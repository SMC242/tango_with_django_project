from django.contrib import admin

from rango.models import Category, Page

@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "url")
    
# Register your models here.
models = [
    Category,
]

for m in models:
    admin.site.register(m)