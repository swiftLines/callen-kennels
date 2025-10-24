from django.contrib import admin
from . import models


@admin.register(models.Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ("title", "is_published", "updated_at")
    list_filter = ("is_published",)
    search_fields = ("title", "body")
    prepopulated_fields = {"slug": ("title",)}
    fields = (
        "title", "slug", "is_published",
        "hero_image",
        "body",
        "image_one", "image_two",   # <- NEW
    )
    

@admin.register(models.Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ("name", "sex", "dob", "retired", "updated_at")
    list_filter = ("sex", "retired")
    search_fields = ("name", "color", "bio")
    prepopulated_fields = {"slug": ("name",)}


class PuppyInline(admin.TabularInline):
    model = models.Puppy
    extra = 0
    fields = ("name", "sex", "color", "price", "status", "main_photo")
    show_change_link = True


@admin.register(models.Litter)
class LitterAdmin(admin.ModelAdmin):
    list_display = ("__str__", "dam", "sire", "status", "expected_date", "whelp_date")
    list_filter = ("status", "dam", "sire")
    search_fields = ("name", "dam__name", "sire__name", "notes")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [PuppyInline]


@admin.register(models.Puppy)
class PuppyAdmin(admin.ModelAdmin):
    list_display = ("__str__", "status", "price", "updated_at")
    list_filter = ("status", "sex", "litter")
    search_fields = ("name", "color", "health_notes")


@admin.register(models.GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "category", "is_published", "created_at")
    list_filter = ("category", "is_published")
    search_fields = ("caption",)


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("title", "start_datetime", "location", "is_published")
    list_filter = ("is_published", "start_datetime")
    search_fields = ("title", "location", "details")


@admin.register(models.SupplyItem)
class SupplyItemAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "price", "in_stock", "is_published")
    list_filter = ("category", "in_stock", "is_published")
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}
