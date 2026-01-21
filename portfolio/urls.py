from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("projects/", views.projects, name="projects"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('blog/', views.blog, name='blog'),
    path('industrial/', views.industrial, name='industrial'),
    path('imprint/', views.imprint, name='imprint'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
]
