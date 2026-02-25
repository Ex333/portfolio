from django.shortcuts import render, get_object_or_404
from .models import (
    Project,
    BlogPost,
    BlogCategory,
    SiteProfile,
    IndustrialPage,
    AboutPage,
    AboutBlock,

)

# ==========================
# BASIC PAGES
# ==========================

def home(request):
    profile = SiteProfile.objects.first()
    return render(request, "home.html", {
        "profile": profile
    })


def projects(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, "projects.html", {
        "projects": projects
    })


def about(request):
    page = AboutPage.objects.first()
    return render(request, "about.html", {
        "page": page
    })


def contact(request):
    return render(request, "contact.html")


def industrial(request):
    page = IndustrialPage.objects.first()
    return render(request, "industrial.html", {
        "page": page
    })


def imprint(request):
    return render(request, "imprint.html")


def privacy_policy(request):
    return render(request, "privacy_policy.html")


# ==========================
# BLOG
# ==========================

def blog(request):
    category_slug = request.GET.get("category")

    categories = BlogCategory.objects.all().order_by("order", "name")

    posts = BlogPost.objects.filter(
        is_published=True
    ).select_related(
        "category"
    ).order_by(
        "-created_at"
    )

    active_category = None

    if category_slug:
        active_category = get_object_or_404(
            BlogCategory,
            slug=category_slug
        )
        posts = posts.filter(category=active_category)

    return render(request, "blog.html", {
        "posts": posts,
        "categories": categories,
        "active_category": active_category,
    })


def blog_detail(request, slug):
    post = get_object_or_404(
        BlogPost.objects
        .select_related("category")
        .prefetch_related("blocks"),
        slug=slug,
        is_published=True
    )

    return render(request, "blog_detail.html", {
        "post": post
    })