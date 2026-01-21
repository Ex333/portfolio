from django.shortcuts import render
from .models import Project

def home(request):
    return render(request, 'home.html')


def projects(request):
    projects = Project.objects.filter(is_published=True)
    return render(request, "projects.html", {
        "projects": projects
    })

def about(request):
    return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

def blog(request):
    return render(request, 'blog.html')

def industrial(request):
    return render(request, 'industrial.html')

def imprint(request):
    return render(request, 'imprint.html')

def privacy_policy(request):
    return render(request, 'privacy_policy.html')