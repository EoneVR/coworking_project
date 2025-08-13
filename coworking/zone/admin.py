from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ['title', 'room_type', 'capacity']
    list_display_links = ['title']
    list_editable = ['capacity']
    ordering = ['title']
    list_filter = ['room_type', 'capacity']
    search_fields = ['title']


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ['title', 'tariff_type', 'price']
    list_display_links = ['title']
    list_editable = ['tariff_type', 'price']
    ordering = ['title']
    list_filter = ['tariff_type', 'price']
    search_fields = ['title', 'description']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['room', 'tariff', 'customer_name', 'start_time', 'end_time']
    list_display_links = ['room', 'tariff']
    list_filter = ['tariff', 'room', 'start_time']
    search_fields = ['customer_name']
    ordering = ['-start_time']
