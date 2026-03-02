from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from .forms import ContactForm
from .models import (
    Project,
    BlogPost,
    BlogCategory,
    SiteProfile,
    IndustrialPage,
    AboutPage,
    AboutBlock,
    HomePage,
)

# ==========================
# BASIC PAGES
# ==========================

def home(request):
    profile = SiteProfile.objects.first()
    page = HomePage.objects.first()

    return render(request, "home.html", {
        "profile": profile,
        "page": page
    })


def projects(request):
    projects_list = (
        Project.objects
        .filter(is_published=True)
        .exclude(url__isnull=True)
        .exclude(url__exact="")
        .order_by("-id")
    )

    paginator = Paginator(projects_list, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "projects.html", {
        "page_obj": page_obj
    })


def about(request):
    page = AboutPage.objects.first()
    return render(request, "about.html", {
        "page": page
    })


# ==========================
# CONTACT
# ==========================

def contact(request):
    if request.method == "POST":
        form = ContactForm(request.POST)

        if form.is_valid():
            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            full_message = f"""
New message from portfolio:

Name: {name}
Email: {email}

Message:
{message}
"""

            send_mail(
                subject="New Contact Form Message",
                message=full_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.DEFAULT_FROM_EMAIL],
            )

            send_mail(
                subject="Thank you for contacting me!",
                message=(
                    "Hi!\n\n"
                    "Thank you for your message. "
                    "I will get back to you as soon as possible.\n\n"
                    "Best regards,\n"
                    "Mateusz"
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

            return redirect("contact_thank_you")

    else:
        form = ContactForm()

    return render(request, "contact.html", {
        "form": form
    })


def contact_thank_you(request):
    return render(request, "contact_thank_you.html")


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
# BLOG (PRODUCTION READY 🔥)
# ==========================

def blog(request):
    category_slug = request.GET.get("category")

    categories = BlogCategory.objects.all()

    posts = (
        BlogPost.objects
        .filter(is_published=True)
        .select_related("category")
        .only(
            "id",
            "title",
            "slug",
            "cover_image",
            "created_at",
            "category__name",
            "category__slug"
        )
        .order_by("-created_at")
    )

    active_category = None

    if category_slug:
        active_category = get_object_or_404(
            BlogCategory,
            slug=category_slug
        )
        posts = posts.filter(category=active_category)

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog.html", {
        "page_obj": page_obj,
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