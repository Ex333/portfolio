import json
import urllib.parse
import urllib.request

from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import Q

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
    Skill
)


# ==========================
# BASIC PAGES
# ==========================

def home(request):

    profile = SiteProfile.objects.first()
    page = HomePage.objects.first()

    skills = Skill.objects.all().order_by("category", "name")

    categories = {}

    for skill in skills:
        categories.setdefault(skill.category, []).append(skill)

    return render(request, "home.html", {
        "profile": profile,
        "page": page,
        "skill_categories": categories
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


def industrial(request):

    page = IndustrialPage.objects.first()

    return render(request, "industrial.html", {
        "page": page
    })


# ==========================
# CONTACT
# ==========================

def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            turnstile_token = request.POST.get("cf-turnstile-response")

            if not turnstile_token:
                return render(request, "contact.html", {
                    "form": form,
                    "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
                    "turnstile_error": "Please complete the verification."
                })

            verification_data = urllib.parse.urlencode({
                "secret": settings.TURNSTILE_SECRET_KEY,
                "response": turnstile_token,
                "remoteip": request.META.get("REMOTE_ADDR"),
            }).encode("utf-8")

            verification_request = urllib.request.Request(
                "https://challenges.cloudflare.com/turnstile/v0/siteverify",
                data=verification_data,
                method="POST"
            )

            try:
                with urllib.request.urlopen(
                    verification_request,
                    timeout=10
                ) as response:

                    verification_result = json.loads(
                        response.read().decode("utf-8")
                    )

            except Exception:
                return render(request, "contact.html", {
                    "form": form,
                    "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
                    "turnstile_error": "Verification failed. Please try again."
                })

            if not verification_result.get("success"):
                return render(request, "contact.html", {
                    "form": form,
                    "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
                    "turnstile_error": "Verification failed. Please try again."
                })

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            full_message = (
                "New message from portfolio:\n\n"
                f"Name: {name}\n"
                f"Email: {email}\n\n"
                "Message:\n"
                f"{message}"
            )

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
        "form": form,
        "turnstile_site_key": settings.TURNSTILE_SITE_KEY,
    })


def contact_thank_you(request):

    return render(request, "contact_thank_you.html")


# ==========================
# LEGAL
# ==========================

def imprint(request):

    return render(request, "imprint.html")


def privacy_policy(request):

    return render(request, "privacy_policy.html")


# ==========================
# BLOG
# ==========================

def blog(request):

    category_slug = request.GET.get("category")
    query = request.GET.get("q")

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

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(category__name__icontains=query)
        )

    paginator = Paginator(posts, 9)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(request, "blog.html", {
        "page_obj": page_obj,
        "categories": categories,
        "active_category": active_category,
        "query": query
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


# ==========================
# TEST ERRORS
# ==========================

# def test403(request):
#     raise PermissionDenied

# def test500(request):
#     x = 1 / 0

# def preview404(request):
#     return render(request, "404.html")