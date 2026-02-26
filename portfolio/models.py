from django.db import models
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile
import os


# ==========================
# SITE PROFILE (HOME PAGE)
# ==========================

class SiteProfile(models.Model):
    name = models.CharField(max_length=100, default="Mateusz")
    hero_title = models.CharField(
        max_length=200,
        default="Hi, I’m Mateusz"
    )
    hero_description = models.TextField(
        default="I build web applications, learn Django and create my developer portfolio."
    )

    hero_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True,
        help_text="Profile photo shown on home page"
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Profile"
# ==========================
# HOME PAGE (DYNAMIC BLOCKS)
# ==========================

class HomePage(models.Model):
    title = models.CharField(max_length=200, default="Home")

    def __str__(self):
        return self.title


class HomeBlock(models.Model):
    page = models.ForeignKey(
        HomePage,
        related_name="blocks",
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField(default=0)

    text = models.TextField(
        blank=True,
        help_text="Optional text content"
    )

    image = models.ImageField(
        upload_to="home/blocks/",
        blank=True,
        null=True
    )

    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Home Block {self.order} for {self.page.title}"

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


class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("devops", "DevOps"),
        ("tools", "Tools"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=64, unique=True, blank=False)
    category = models.CharField(
        max_length=40,
        choices=CATEGORY_CHOICES,
        default="other"
    )
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="skills/", blank=True, null=True)

    def __str__(self):
        return self.name


class SkillRequirement(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanced"),
    ]

    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField(blank=True)


# ==========================
# BLOG CATEGORIES
# ==========================

class BlogCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name


# ==========================
# BLOG
# ==========================

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts"
    )

    cover_image = models.ImageField(
        upload_to="blog/covers/",
        blank=True,
        null=True,
        help_text="Main image shown on blog list"
    )

    # 🔥 NOWE POLE MINIATURY
    thumbnail = models.ImageField(
        upload_to="blog/thumbnails/",
        blank=True,
        null=True,
        editable=False
    )

    content = models.TextField(blank=True)

    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.cover_image:
            img = Image.open(self.cover_image.path)

            max_width = 600  # 🔥 szerokość miniatury

            if img.width > max_width:
                ratio = max_width / float(img.width)
                new_height = int(float(img.height) * ratio)

                img = img.resize((max_width, new_height), Image.LANCZOS)

            # 🔥 konwertujemy do JPEG i kompresujemy
            thumb_io = BytesIO()
            img.convert("RGB").save(thumb_io, format="JPEG", quality=85)

            filename = os.path.basename(self.cover_image.name)
            thumb_name = f"thumb_{filename}"

            self.thumbnail.save(
                thumb_name,
                ContentFile(thumb_io.getvalue()),
                save=False
            )

            super().save(update_fields=["thumbnail"])

    def __str__(self):
        return self.title
# ==========================
# CONTENT BLOCKS
# ==========================

class BlogBlock(models.Model):
    post = models.ForeignKey(
        BlogPost,
        related_name="blocks",
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField(
        help_text="Order of this block inside the post"
    )

    text = models.TextField(
        blank=True,
        help_text="Text content for this block (optional)"
    )

    image = models.ImageField(
        upload_to="blog/blocks/",
        blank=True,
        null=True,
        help_text="Image for this block (optional)"
    )

    alt_text = models.CharField(
        max_length=200,
        blank=True
    )

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Block {self.order} for {self.post.title}"

# ==========================
# INDUSTRIAL PAGE
# ==========================

class IndustrialPage(models.Model):
    title = models.CharField(max_length=200, default="Industrial Experience")
    subtitle = models.TextField(blank=True)

    def __str__(self):
        return self.title


class IndustrialBlock(models.Model):
    page = models.ForeignKey(
        IndustrialPage,
        related_name="blocks",
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField()

    text = models.TextField(blank=True)
    image = models.ImageField(
        upload_to="industrial/blocks/",
        blank=True,
        null=True
    )

    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Block {self.order} for {self.page.title}"


# ==========================
# ABOUT PAGE
# ==========================

class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About Me")
    subtitle = models.TextField(blank=True)

    def __str__(self):
        return self.title


class AboutBlock(models.Model):
    page = models.ForeignKey(
        AboutPage,
        related_name="blocks",
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField()

    text = models.TextField(blank=True)

    image = models.ImageField(
        upload_to="about/blocks/",
        blank=True,
        null=True
    )

    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Block {self.order} for {self.page.title}"