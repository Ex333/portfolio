from django.db import models
from PIL import Image
import os
from django_ckeditor_5.fields import CKEditor5Field


# ==========================
# SITE PROFILE
# ==========================

class SiteProfile(models.Model):
    name = models.CharField(max_length=100, default="Mateusz")

    hero_title = models.CharField(
        max_length=200,
        default="Hi, I’m Mateusz"
    )

    hero_description = CKEditor5Field(
        'Hero description',
        config_name='default'
    )

    hero_image = models.ImageField(
        upload_to="profile/",
        blank=True,
        null=True
    )

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "Site Profile"


# ==========================
# HOME PAGE
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

    text = CKEditor5Field(
        'Text',
        config_name='default',
        blank=True
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
        return f"Home Block {self.order}"


# ==========================
# PROJECTS
# ==========================

class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)

    short_description = models.CharField(max_length=300)

    description = CKEditor5Field(
        'Description',
        config_name='default'
    )

    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        null=True
    )

    url = models.URLField(blank=True, null=True)

    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title


# ==========================
# SKILLS
# ==========================

class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("devops", "DevOps"),
        ("tools", "Tools"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=64, unique=True)

    category = models.CharField(
        max_length=40,
        choices=CATEGORY_CHOICES,
        default="other"
    )

    description = CKEditor5Field(
        'Description',
        config_name='default',
        blank=True
    )

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

    level = models.CharField(
        max_length=20,
        choices=LEVEL_CHOICES
    )

    description = CKEditor5Field(
        'Description',
        config_name='default',
        blank=True
    )


# ==========================
# BLOG CATEGORY
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
# BLOG POST
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
        null=True
    )

    content = CKEditor5Field(
        'Content',
        config_name='default'
    )

    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.cover_image:
            img = Image.open(self.cover_image.path)

            max_width = 1600

            if img.width > max_width:
                ratio = max_width / float(img.width)
                new_height = int(img.height * ratio)

                img = img.resize((max_width, new_height), Image.LANCZOS)

            img = img.convert("RGB")

            img.save(
                self.cover_image.path,
                format="JPEG",
                quality=82,
                optimize=True
            )

    def delete(self, *args, **kwargs):
        if self.cover_image:
            if os.path.isfile(self.cover_image.path):
                os.remove(self.cover_image.path)

        super().delete(*args, **kwargs)

    def __str__(self):
        return self.title


# ==========================
# BLOG BLOCKS
# ==========================

class BlogBlock(models.Model):
    post = models.ForeignKey(
        BlogPost,
        related_name="blocks",
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField()

    text = CKEditor5Field(
        'Text',
        config_name='default',
        blank=True
    )

    image = models.ImageField(
        upload_to="blog/blocks/",
        blank=True,
        null=True
    )

    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"Block {self.order} for {self.post.title}"


# ==========================
# INDUSTRIAL PAGE
# ==========================

class IndustrialPage(models.Model):
    title = models.CharField(max_length=200, default="Industrial Experience")

    subtitle = CKEditor5Field(
        'Subtitle',
        config_name='default',
        blank=True
    )

    def __str__(self):
        return self.title


class IndustrialBlock(models.Model):
    page = models.ForeignKey(
        IndustrialPage,
        related_name="blocks",
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField()

    text = CKEditor5Field(
        'Text',
        config_name='default',
        blank=True
    )

    image = models.ImageField(
        upload_to="industrial/blocks/",
        blank=True,
        null=True
    )

    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order"]


# ==========================
# ABOUT PAGE
# ==========================

class AboutPage(models.Model):
    title = models.CharField(max_length=200, default="About Me")

    subtitle = CKEditor5Field(
        'Subtitle',
        config_name='default',
        blank=True
    )

    def __str__(self):
        return self.title


class AboutBlock(models.Model):
    page = models.ForeignKey(
        AboutPage,
        related_name="blocks",
        on_delete=models.CASCADE
    )

    order = models.PositiveIntegerField()

    text = CKEditor5Field(
        'Text',
        config_name='default',
        blank=True
    )

    image = models.ImageField(
        upload_to="about/blocks/",
        blank=True,
        null=True
    )

    alt_text = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ["order"]