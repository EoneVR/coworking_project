from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Coffee)
class CoffeeAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'size', 'unit_price']
    list_editable = ['unit_price']
    list_per_page = 20
    search_fields = ['title']


@admin.register(Bakery)
class BakeryAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title']
    }
    list_display = ['title', 'unit_price', 'in_stock']
    list_display_links = ['title']
    list_editable = ['unit_price', 'in_stock']
    list_per_page = 20
    search_fields = ['title', 'unit_price']
    ordering = ['title']

