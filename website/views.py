from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.utils import timezone
from .models import Page, Dog, Litter, Puppy, GalleryImage, Event, SupplyItem, Homepage, AboutPage, AboutBreedPage, PuppiesPage, SuppliesPage,GirlsPage, BoysPage, PastLittersPage, PastPuppy


class HomeView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["home"] = Homepage.objects.first()
        # ctx["available_puppies"] = Puppy.objects.filter(status=Puppy.AVAILABLE)[:6]
        # ctx["upcoming_litters"] = Litter.objects.filter(status=Litter.UPCOMING).order_by("expected_date")[:3]
        # ctx["grown_images"] = GalleryImage.objects.filter(is_published=True, category=GalleryImage.GROWN)[:8]
        # ctx["next_events"] = Event.objects.filter(is_published=True, start_datetime__gte=timezone.now()).order_by("start_datetime")[:3]
        return ctx


class PageDetailView(DetailView):
    model = Page
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "website/page_detail.html"
    context_object_name = "page"
    queryset = Page.objects.filter(is_published=True)

    def get_template_names(self):
        obj = getattr(self, "object", None) or self.get_object()
        if obj.slug == "about":
            return ["website/about.html"]
        return [self.template_name]
    

# Dogs
class GirlsListView(ListView):
    model = Dog
    template_name = "website/dogs_girls.html"
    context_object_name = "dogs"
    queryset = Dog.objects.filter(sex=Dog.FEMALE).order_by("name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["girls_page"] = GirlsPage.objects.first()
        return ctx
    

class BoysListView(ListView):
    model = Dog
    template_name = "website/dogs_boys.html"
    context_object_name = "dogs"
    queryset = Dog.objects.filter(sex=Dog.MALE).order_by("name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["boys_page"] = BoysPage.objects.first()
        return ctx


class DogDetailView(DetailView):
    model = Dog
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "website/dog_detail.html"


# Litters & Puppies
class PuppyAvailableListView(ListView):
    model = Puppy
    template_name = "website/puppies_available.html"
    context_object_name = "puppies"
    queryset = Puppy.objects.filter(status=Puppy.AVAILABLE).select_related("litter", "litter__dam", "litter__sire")


class LitterUpcomingListView(ListView):
    model = Litter
    template_name = "website/litters_upcoming.html"
    context_object_name = "litters"
    queryset = Litter.objects.filter(status=Litter.UPCOMING).select_related("dam", "sire").order_by("expected_date")


class LitterPastListView(ListView):
    model = PastPuppy
    template_name = "website/litters_past.html"
    context_object_name = "past_puppies"

    def get_queryset(self):
        return PastPuppy.objects.filter(is_published=True).order_by("-birth_date", "name")


    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["past_litters_page"] = PastLittersPage.objects.first()
        return ctx


# Gallery
class GrownGalleryListView(ListView):
    model = GalleryImage
    template_name = "website/gallery_grown.html"
    context_object_name = "images"
    queryset = GalleryImage.objects.filter(is_published=True, category=GalleryImage.GROWN).order_by("-created_at")


# Events
class EventListView(ListView):
    model = Event
    template_name = "website/events_list.html"
    context_object_name = "events"
    queryset = Event.objects.filter(is_published=True).order_by("start_datetime")


# Supplies
class SupplyListView(ListView):
    model = SupplyItem
    template_name = "website/supplies_list.html"
    context_object_name = "items"
    queryset = SupplyItem.objects.filter(is_published=True).order_by("name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["supplies_page"] = SuppliesPage.objects.first()
        return ctx

class SupplyDetailView(DetailView):
    model = SupplyItem
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "website/supply_detail.html"


class AboutPageView(TemplateView):
    template_name = "website/about.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["about"] = AboutPage.objects.first()
        return ctx
    

class AboutBreedPageView(TemplateView):
    template_name = "website/about_breed.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["breed"] = AboutBreedPage.objects.first()
        return ctx


class PuppyAvailableListView(ListView):
    model = Puppy
    template_name = "website/puppies_available.html"
    context_object_name = "puppies"

    def get_queryset(self):
        return Puppy.objects.filter(status=Puppy.AVAILABLE).order_by("name")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["puppies_page"] = PuppiesPage.objects.first()
        return ctx
