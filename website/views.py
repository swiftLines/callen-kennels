from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView, DetailView, ListView
from django.utils import timezone
from .models import Page, Dog, Litter, Puppy, GalleryImage, Event, SupplyItem


class HomeView(TemplateView):
    template_name = "website/home.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["available_puppies"] = Puppy.objects.filter(status=Puppy.AVAILABLE)[:6]
        ctx["upcoming_litters"] = Litter.objects.filter(status=Litter.UPCOMING).order_by("expected_date")[:3]
        ctx["grown_images"] = GalleryImage.objects.filter(is_published=True, category=GalleryImage.GROWN)[:8]
        ctx["next_events"] = Event.objects.filter(is_published=True, start_datetime__gte=timezone.now()).order_by("start_datetime")[:3]
        return ctx


class PageDetailView(DetailView):
    model = Page
    # slug_field = "slug"
    # slug_url_kwarg = "slug"
    template_name = "website/page_detail.html"
    queryset = Page.objects.filter(is_published=True)

    def get_object(self):
        return get_object_or_404(Page, slug=self.kwargs["slug"], is_published=True)

# Dogs
class GirlsListView(ListView):
    model = Dog
    template_name = "website/dogs_girls.html"
    context_object_name = "dogs"
    queryset = Dog.objects.filter(sex=Dog.FEMALE).order_by("name")


class BoysListView(ListView):
    model = Dog
    template_name = "website/dogs_boys.html"
    context_object_name = "dogs"
    queryset = Dog.objects.filter(sex=Dog.MALE).order_by("name")


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
    model = Litter
    template_name = "website/litters_past.html"
    context_object_name = "litters"
    queryset = Litter.objects.filter(status=Litter.PAST).select_related("dam", "sire").order_by("-whelp_date", "-created_at")


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


class SupplyDetailView(DetailView):
    model = SupplyItem
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "website/supply_detail.html"
