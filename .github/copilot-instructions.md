# Copilot Instructions for Portfolio Project

## Project Overview
A Django-based personal portfolio website showcasing projects and skills. Single-app architecture (`portfolio` app) with template-based rendering and SQLite database.

**Tech Stack:** Django 5.2, SQLite3, vanilla HTML/CSS

## Architecture & Key Components

### Django Models (`portfolio/models.py`)
- **Project**: Portfolio projects with slug, short_description, description, image, URL, publication status, and ordering
- **Skill**: Technical skills with categories (frontend/backend/devops/tools/other) and optional photo
- **SkillRequirement**: Links skills to projects with proficiency levels (beginner/intermediate/advanced)
- **Me**: Personal profile data (name, bio, photo, email, phone)

**Key Patterns:**
- Projects ordered by `order` field (manual priority), then by creation date descending
- Published projects filtered via `is_published=True` in views
- Use `slug` field for clean URLs (currently not implemented in routes)
- All models have `__str__()` for admin readability

### Views & Routing (`portfolio/views.py`, `portfolio/urls.py`)
- Simple function-based views, no API endpoints
- Projects view filters published items: `Project.objects.filter(is_published=True)`
- Root config URLconf (`config/urls.py`) includes portfolio URLs at empty path
- Static pages (about, blog, industrial, imprint, privacy_policy) currently return empty templates

### Templates (`templates/base.html` + individual pages)
- Uses Django template tags: `{% load static %}`, `{% block %}` for inheritance
- Base template provides navbar navigation and metadata
- Individual pages extend base.html with content blocks
- Static assets served from `portfolio/static/`

## Common Development Workflows

### Running the Server
```bash
python manage.py runserver
```
Starts development server on `http://localhost:8000`

### Database Operations
```bash
python manage.py makemigrations    # Create migration files
python manage.py migrate           # Apply migrations
python manage.py createsuperuser   # Create admin user
python manage.py shell             # Django shell for testing
```

### Admin Interface
Access at `/admin/` after creating superuser. All models registered via `portfolio/admin.py`.

## Project-Specific Conventions

1. **Image Uploads:** Media files stored in `media/` directory with subdirectories per model type (`projects/`, `skills/`, `me/`)
2. **Slug Fields:** Use `SlugField(unique=True)` for clean URLs on Project model
3. **Ordering:** Project display uses `order` field (0-indexed) with `-created_at` as tiebreaker
4. **Polish Text:** Help texts and category descriptions in Polish (e.g., "Krótki opis widoczny na liście projektów")
5. **Publication Control:** Use `is_published` flag for content visibility, don't delete projects

## File Organization
- `config/`: Django settings and URL routing
- `portfolio/`: Main app (models, views, admin config)
- `portfolio/migrations/`: Database schema history
- `portfolio/static/css/`: Stylesheet (main.css)
- `templates/`: HTML templates for all views
- `media/`: User-uploaded images (gitignored typically)
- `db.sqlite3`: Development database

## Current Development State
- Basic CMS functionality implemented
- Static pages created but empty (need content in blog.html, industrial.html)
- Admin interface fully customized with fieldsets, filters, search, and inline editing (see `portfolio/admin.py`)
- No API endpoints or AJAX functionality
- Template-only rendering (no JavaScript frameworks)

## Important Notes for AI Agents
- **SECRET_KEY exposed** in settings.py (change before production)
- **DEBUG = True** in development settings
- **ALLOWED_HOSTS empty** (configure before deployment)
- **No authentication system** implemented (all views public)
- When adding models, create migrations and add to admin interface
- Template context data is minimal—avoid assuming complex view logic
