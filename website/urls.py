from django.urls import path
from . import views

urlpatterns = [
    path("", views.HomeView.as_view(), name="home"),

    # About / Breed info / Contact (use Page model slugs)
    path("page/<slug:slug>/", views.PageDetailView.as_view(), name="page_detail"),

    # Puppies & Litters
    path("puppies/available/", views.PuppyAvailableListView.as_view(), name="puppies_available"),
    path("litters/upcoming/", views.LitterUpcomingListView.as_view(), name="litters_upcoming"),
    path("litters/past/", views.LitterPastListView.as_view(), name="litters_past"),

    # Dogs
    path("dogs/girls/", views.GirlsListView.as_view(), name="dogs_girls"),
    path("dogs/boys/", views.BoysListView.as_view(), name="dogs_boys"),
    path("dogs/<slug:slug>/", views.DogDetailView.as_view(), name="dog_detail"),

    # Gallery
    path("gallery/grown/", views.GrownGalleryListView.as_view(), name="gallery_grown"),

    # Events
    path("ruff-house/venues/", views.EventListView.as_view(), name="events_list"),

    # Supplies (catalog)
    path("ruff-house/supplies/", views.SupplyListView.as_view(), name="supplies_list"),
    path("ruff-house/supplies/<slug:slug>/", views.SupplyDetailView.as_view(), name="supply_detail"),
]
