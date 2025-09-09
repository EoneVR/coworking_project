from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ("title", "duration", "price")
    list_filter = ("duration",)
    search_fields = ("title",)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    list_display = ("user", "subscription", "start_date", "end_date", "is_active_display")
    list_filter = ("subscription__duration", "start_date", "end_date")
    search_fields = ("user__username", "subscription__title")

    def is_active_display(self, obj):
        return obj.is_active
    is_active_display.short_description = "Активна"
    is_active_display.boolean = True


@admin.register(Tariff)
class TariffAdmin(admin.ModelAdmin):
    list_display = ("title", "room_type", "price_per_hour")
    list_filter = ("room_type",)
    search_fields = ("title",)


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("title", "room_type", "capacity")
    list_filter = ("room_type", "capacity")
    search_fields = ("title",)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "room", "start_time", "end_time", "subscription", "price")
    list_filter = ("room__room_type", "start_time", "end_time")
    search_fields = ("user__username", "room__title")
