from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# ---- Pages / Simple Content ----
class Page(TimeStampedModel):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    hero_image = models.ImageField(upload_to="pages/hero/", blank=True, null=True)
    body = models.TextField(blank=True)

    # NEW
    image_one = models.ImageField(upload_to="pages/about/", blank=True, null=True)
    image_two = models.ImageField(upload_to="pages/about/", blank=True, null=True)

    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:220]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("page_detail", kwargs={"slug": self.slug})


# ---- Dogs / Litters / Puppies ----
class Dog(TimeStampedModel):
    FEMALE = "F"
    MALE = "M"
    SEX_CHOICES = [(FEMALE, "Female"), (MALE, "Male")]

    name = models.CharField(max_length=120)
    slug = models.SlugField(max_length=140, unique=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    dob = models.DateField(blank=True, null=True)
    color = models.CharField(max_length=120, blank=True)
    bio = models.TextField(blank=True)

    photo = models.ImageField(upload_to="dogs/photos/", blank=True, null=True)
    retired = models.BooleanField(default=False)

    class Meta:
        ordering = ["name"]
        verbose_name = "Dog"
        verbose_name_plural = "Dogs"

    def __str__(self):
        return f"{self.name} ({self.get_sex_display()})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:140]
        super().save(*args, **kwargs)

    @property
    def is_girl(self):
        return self.sex == self.FEMALE

    @property
    def is_boy(self):
        return self.sex == self.MALE


class Litter(TimeStampedModel):
    UPCOMING = "UPCOMING"
    PAST = "PAST"
    STATUS_CHOICES = [(UPCOMING, "Upcoming"), (PAST, "Past")]

    name = models.CharField(
        max_length=140,
        help_text="Optional display name (e.g., 'Spring 2025 – Daisy × Max')",
        blank=True,
    )
    slug = models.SlugField(max_length=160, unique=True, blank=True)

    dam = models.ForeignKey(Dog, on_delete=models.PROTECT, related_name="litters_as_dam")
    sire = models.ForeignKey(Dog, on_delete=models.PROTECT, related_name="litters_as_sire")

    expected_date = models.DateField(blank=True, null=True)
    whelp_date = models.DateField(blank=True, null=True)
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=UPCOMING)

    class Meta:
        ordering = ["-expected_date", "-whelp_date", "-created_at"]

    def __str__(self):
        label = self.name or f"{self.dam.name} × {self.sire.name}"
        return f"{label} ({self.status})"

    def save(self, *args, **kwargs):
        if not self.slug:
            base = self.name or f"{self.dam.name}-{self.sire.name}"
            self.slug = slugify(base)[:160]
        super().save(*args, **kwargs)

    @property
    def available_puppies(self):
        return self.puppies.filter(status=Puppy.AVAILABLE)


class Puppy(TimeStampedModel):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    SOLD = "SOLD"
    STATUS_CHOICES = [
        (AVAILABLE, "Available"),
        (RESERVED, "Reserved"),
        (SOLD, "Sold"),
    ]

    FEMALE = "F"
    MALE = "M"
    SEX_CHOICES = [(FEMALE, "Female"), (MALE, "Male")]

    litter = models.ForeignKey(Litter, on_delete=models.CASCADE, related_name="puppies")
    name = models.CharField(max_length=120, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, blank=True)
    color = models.CharField(max_length=120, blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=AVAILABLE)

    main_photo = models.ImageField(upload_to="puppies/main/", blank=True, null=True)
    health_notes = models.TextField(blank=True)
    contract_pdf = models.FileField(upload_to="puppies/contracts/", blank=True, null=True)

    class Meta:
        ordering = ["litter", "name"]

    def __str__(self):
        base = self.name or "Puppy"
        return f"{base} – {self.litter}"


# ---- Galleries ----
class GalleryImage(TimeStampedModel):
    GROWN = "grown"
    GENERAL = "general"
    CATEGORY_CHOICES = [
        (GROWN, "Grown Pics"),
        (GENERAL, "General"),
    ]

    category = models.CharField(max_length=32, choices=CATEGORY_CHOICES, default=GENERAL)
    image = models.ImageField(upload_to="gallery/", blank=True, null=True)
    caption = models.CharField(max_length=200, blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.caption or f"Image #{self.pk}"


# ---- Events (Ruff House) ----
class Event(TimeStampedModel):
    title = models.CharField(max_length=200)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=200, blank=True)
    details = models.TextField(blank=True)
    map_link = models.URLField(blank=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["start_datetime"]

    def __str__(self):
        return self.title


# ---- Supplies (catalog only) ----
class SupplyItem(TimeStampedModel):
    name = models.CharField(max_length=180)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="supplies/", blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.CharField(max_length=120, blank=True)
    in_stock = models.BooleanField(default=True)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:200]
        super().save(*args, **kwargs)


class Homepage(models.Model):
    # Top heading
    heading = models.CharField(max_length=200, default="Welcome to Callen Kennels & Ruff House Dog Supplies LLC!")

    # Left block (Callen Kennels)
    left_title = models.CharField(max_length=120, default="Callen Kennels")
    left_blurb = models.TextField(blank=True)
    left_image = models.ImageField(upload_to="home/", blank=True, null=True)
    left_link = models.CharField(
        max_length=200,
        default="/page/about/",  # you can store a URL or a path here
        help_text="Internal path or full URL (e.g. /page/about/ or https://...)",
    )

    # Right block (Ruff House)
    right_title = models.CharField(max_length=160, default="Ruff House Dog Supplies LLC")
    right_blurb = models.TextField(blank=True)
    right_image = models.ImageField(upload_to="home/", blank=True, null=True)
    right_link = models.CharField(
        max_length=200,
        default="/ruff-house/supplies/",
        help_text="Internal path or full URL",
    )

    # Contact block
    contact_heading = models.CharField(max_length=120, default="Contact Information")
    contact_name = models.CharField(max_length=120, default="Sue Callen")
    contact_phone = models.CharField(max_length=60, blank=True, default="518-XXX-XXXX")
    contact_email = models.EmailField(blank=True, default="tsuc4954@gmail.com")
    contact_address = models.CharField(max_length=200, blank=True, default="140 Littner Rd, Rensselaerville, NY")

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Homepage"
        verbose_name_plural = "Homepage"

    def __str__(self):
        return "Homepage content"
    