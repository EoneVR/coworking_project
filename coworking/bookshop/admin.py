from django.contrib import admin
from .models import Category, Book


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title']
    list_display_links = ['id', 'title']
    list_per_page = 20
    search_fields = ['title']
    list_filter = ['title']
    ordering = ['title']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'year_of_publish', 'category', 'unit_price', 'in_stock']
    list_display_links = ['title', 'author', 'year_of_publish', 'category']
    list_editable = ['unit_price', 'in_stock']
    list_per_page = 20
    search_fields = ['title', 'author', 'description']
    list_filter = ['binding', 'year_of_publish', 'in_stock']
    ordering = ['-year_of_publish', 'title']
