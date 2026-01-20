from django.contrib import admin
from .models import Project, Skill, SkillRequirement


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "is_published",
        "order",
        "created_at",
    )

    list_filter = (
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
        "short_description",
        "description",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    list_editable = (
        "is_published",
        "order",
    )

    ordering = (
        "order",
        "-created_at",
    )

    fieldsets = (
        ("Podstawowe informacje", {
            "fields": (
                "title",
                "slug",
                "short_description",
                "description",
                "image",
            )
        }),
        ("Linki", {
            "fields": (
                "url",
            )
        }),
        ("Publikacja", {
            "fields": (
                "is_published",
                "order",
            )
        }),
        ("Daty", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    readonly_fields = (
        "created_at",
        "updated_at",
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
    )

    list_filter = (
        "category",
    )

    search_fields = (
        "name",
        "description",
    )

    ordering = (
        "name",
    )


@admin.register(SkillRequirement)
class SkillRequirementAdmin(admin.ModelAdmin):
    list_display = (
        "skill",
        "level",
    )

    list_filter = (
        "level",
        "skill",
    )

    search_fields = (
        "description",
        "skill__name",
    )

    ordering = (
        "skill",
        "level",
    )
