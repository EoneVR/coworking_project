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

