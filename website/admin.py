from django import forms
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
    fields = ("name", "sex", "color", "price", "status", "photo_1")
    show_change_link = True


# @admin.register(models.Litter)
# class LitterAdmin(admin.ModelAdmin):
#     list_display = ("__str__", "dam", "sire", "status", "expected_date", "whelp_date")
#     list_filter = ("status", "dam", "sire")
#     search_fields = ("name", "dam__name", "sire__name", "notes")
#     prepopulated_fields = {"slug": ("name",)}
#     inlines = [PuppyInline]


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
        ("Header", {"fields": ("heading", "subheading")}),

        ("Top images (big logos)", {"fields": ("left_image", "right_image")}),

        ("Left block (Callen Kennels)", {
            "fields": (
                "left_small_logo",
                "left_title",
                "left_blurb",
                "left_link",
                "left_button_label",
            )
        }),

        ("Right block (Ruff House)", {
            "fields": (
                "right_small_logo",
                "right_title",
                "right_blurb",
                "right_link",
                "right_button_label",
            )
        }),

        ("Contact", {
            "fields": (
                "contact_heading",
                "contact_name",
                "contact_phone",
                "contact_email",
                "contact_address",
            )
        }),
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


@admin.register(models.AboutBreedPage)
class AboutBreedPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    fieldsets = (
        (None, {"fields": ("title", "header_image", "intro_paragraph")}),
        ("Breed Details", {
            "fields": (
                "height",
                "weight",
                "colors",
                "eyes",
                "coat",
                "temperament",
                "breed_tendencies",
                "exercise_needed",
            )
        }),
    )

    def has_add_permission(self, request):
        # only one record
        if models.AboutBreedPage.objects.exists():
            return False
        return super().has_add_permission(request)
    

@admin.register(models.PuppiesPage)
class PuppiesPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    fields = ("title", "heading", "header_image")

    def has_add_permission(self, request):
        # only one settings row
        if models.PuppiesPage.objects.exists():
            return False
        return super().has_add_permission(request)


class UpcomingEventInlineForm(forms.ModelForm):
    class Meta:
        model = models.UpcomingEvent
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Accept 12-hour input
        for f in ("start_time", "end_time"):
            self.fields[f].input_formats = ["%I:%M %p"]
            self.fields[f].help_text = "Example: 10:00 AM"

            self.fields[f].widget = forms.TimeInput(
                format="%I:%M %p",
                attrs={"placeholder": "10:00 AM"}
            )


class UpcomingEventInline(admin.TabularInline):
    model = models.UpcomingEvent
    form = UpcomingEventInlineForm
    extra = 0
    fields = ("sort_order", "is_active", "name", "location", "start_date", "end_date", "start_time", "end_time")
    ordering = ("sort_order", "start_date", "start_time")

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        formfield = super().formfield_for_dbfield(db_field, request, **kwargs)

        if db_field.name in ("start_time", "end_time"):
            formfield.widget = forms.TextInput(attrs={"placeholder": "10:00 AM"})
        return formfield


@admin.register(models.SuppliesPage)
class SuppliesPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    fields = (
        "title", 
        "heading", 
        "header_image",
        
        # Box 1 (How to Purchase)
        "show_box_1",
        "box_1_title",
        "box_1_body",

        # Box 2 (Upcoming Events)
        "show_box_2",
        "box_2_title",
        )

    # allow managing the dates list inline (and optionally a 2nd inline if you created a 2nd related model)
    inlines = [UpcomingEventInline]

    def has_add_permission(self, request):
        if models.SuppliesPage.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(models.GirlsPage)
class GirlsPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    fields = ("title", "heading", "header_image")

    def has_add_permission(self, request):
        if models.GirlsPage.objects.exists():
            return False
        return super().has_add_permission(request)

@admin.register(models.BoysPage)
class BoysPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    fields = ("title", "heading", "header_image")

    def has_add_permission(self, request):
        if models.BoysPage.objects.exists():
            return False
        return super().has_add_permission(request)
    

@admin.register(models.PastLittersPage)
class PastLittersPageAdmin(admin.ModelAdmin):
    list_display = ("__str__", "updated_at")
    fields = ("title", "heading", "header_image")

    def has_add_permission(self, request):
        if models.PastLittersPage.objects.exists():
            return False
        return super().has_add_permission(request)


@admin.register(models.PastPuppy)
class PastPuppyAdmin(admin.ModelAdmin):
    list_display = ("name", "litter_name", "birth_date", "is_published")
    list_filter = ("is_published",)
    search_fields = ("name", "litter_name")
    fields = (
        "name",
        "litter_name",
        "birth_date",
        "puppy_photo",
        "adult_photo",
        "is_published",
    )
