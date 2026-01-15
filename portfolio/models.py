from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    short_description = models.CharField(
        max_length=300,
        help_text="Krótki opis widoczny na liście projektów"
    )
    description = models.TextField()

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True
    )

    url = models.URLField(
        blank=True,
        null=True,
        help_text="Link do live demo lub repozytorium"
    )

    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title
