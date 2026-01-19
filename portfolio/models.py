from django.db import models



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

from django.db import models


class Skill(models.Model):
    CATEGORY_CHOICES = [
      ("frontend", "Frontend"),
      ("backend", "Backend"),
      ("devops", "DevOps"),
      ("tools", "Tools"),
      ("other", "Other"),
  ]
    name = models.CharField(max_length=64, unique=True,blank=False)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES,default="other")
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to="skills/", blank=True, null=True)

    def __str__(self):
        return self.name
        

class SkillRequirement(models.Model):
    LEVEL_CHOICES = [
        ("beginner", "Beginner"),
        ("intermediate", "Intermediate"),
        ("advanced", "Advanmced"),
    ]
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    description = models.TextField(blank=True)
