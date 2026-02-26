from django.urls import path
from . import views

urlpatterns = [
    # ==========================
    # BASIC PAGES
    # ==========================
    path("", views.home, name="home"),
    path("projects/", views.projects, name="projects"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("contact/thank-you/", views.contact_thank_you, name="contact_thank_you"),
    # ==========================
    # BLOG
    # ==========================
    path("blog/", views.blog, name="blog"),
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),

    # ==========================
    # LEGAL / OTHER
    # ==========================
    path("industrial/", views.industrial, name="industrial"),
    path("imprint/", views.imprint, name="imprint"),
    path("privacy-policy/", views.privacy_policy, name="privacy_policy"),
]
