from django.contrib import admin
from .models import Wine, Store, StoreWine


@admin.register(Wine)
class WineAdmin(admin.ModelAdmin):
    list_display = ("name", "manufacturer", "type", "is_vintage", "sweetness", "price")
    list_filter = ("type", "is_vintage", "sweetness")
    search_fields = ("name", "manufacturer")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address")


@admin.register(StoreWine)
class StoreWineAdmin(admin.ModelAdmin):
    list_display = ("store", "wine", "quantity")
    list_filter = ("store", "wine")
