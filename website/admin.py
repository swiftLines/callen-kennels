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


@admin.register(models.Homepage)
class HomepageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    fieldsets = (
        (None, {"fields": ("heading",)}),
        ("Left block (Callen Kennels)", {"fields": ("left_title","left_blurb","left_image","left_link", "left_button_label")}),
        ("Right block (Ruff House)", {"fields": ("right_title","right_blurb","right_image","right_link", "right_button_label")}),
        ("Contact", {"fields": ("contact_heading","contact_name","contact_phone","contact_email","contact_address")}),
    )

    def has_add_permission(self, request):
        # Allow only one row
        if models.Homepage.objects.exists():
            return False
        return super().has_add_permission(request)
    

@admin.register(models.AboutPage)
class AboutPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "header_image", "intro_paragraph", "body_paragraph")}),
        ("Gallery", {"fields": ("image_1", "image_2")}),
    )

    def has_add_permission(self, request):
        # Only one About page
        if models.AboutPage.objects.exists():
            return False
        return super().has_add_permission(request)
