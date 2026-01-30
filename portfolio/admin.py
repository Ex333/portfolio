from django.contrib import admin
from .models import (
    Project,
    Skill,
    SkillRequirement,
    BlogCategory,
    BlogPost,
    BlogBlock,
)


# ==========================
# PROJECTS
# ==========================

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
        ("Basic information", {
            "fields": (
                "title",
                "slug",
                "short_description",
                "description",
                "image",
            )
        }),
        ("Links", {
            "fields": (
                "url",
            )
        }),
        ("Publication", {
            "fields": (
                "is_published",
                "order",
            )
        }),
        ("Dates", {
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


# ==========================
# SKILLS
# ==========================

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


# ==========================
# BLOG CATEGORIES
# ==========================

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "order",
    )

    prepopulated_fields = {
        "slug": ("name",)
    }

    list_editable = (
        "order",
    )

    ordering = (
        "order",
        "name",
    )


# ==========================
# BLOG BLOCKS INLINE
# ==========================

class BlogBlockInline(admin.TabularInline):
    model = BlogBlock
    extra = 1
    ordering = ("order",)

    fields = (
        "order",
        "text",
        "image",
        "alt_text",
    )


# ==========================
# BLOG POSTS
# ==========================

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "category",
        "is_published",
        "created_at",
    )

    list_filter = (
        "category",
        "is_published",
        "created_at",
    )

    search_fields = (
        "title",
    )

    prepopulated_fields = {
        "slug": ("title",)
    }

    inlines = [
        BlogBlockInline,
    ]

    ordering = (
        "-created_at",
    )

    fieldsets = (
        ("Post", {
            "fields": (
                "title",
                "slug",
                "category",
                "cover_image",
            )
        }),
        ("Publication", {
            "fields": (
                "is_published",
            )
        }),
        ("Dates", {
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
