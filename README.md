# 🚀 Professional Blog API - Django REST Framework

A feature-rich, production-ready Blog API built with Django REST Framework, featuring JWT authentication, advanced filtering, likes, bookmarks, and comprehensive documentation.

## ✨ Features

### 🔐 Authentication & Authorization
- JWT (JSON Web Token) authentication
- Token refresh mechanism
- User registration with email validation
- Password change functionality
- Role-based permissions (Admin/User)

### 📝 Article Management
- Full CRUD operations for articles
- Rich text content with HTML sanitization
- Automatic slug generation
- Featured images support
- Draft/Published status
- View count tracking
- SEO-friendly excerpts
- Estimated reading time

### 🏷️ Tag System
- Flexible tagging system
- Tag-based filtering
- Popular tags listing
- Articles by tag endpoint

### 💬 Comment System
- Nested comments (replies)
- Comment editing with edit tracking
- Comment deletion (owner or admin)
- Real-time comment counts

### ❤️ Engagement Features
- Article likes/unlikes
- Bookmark system for saving articles
- Like counts and user lists
- Bookmark management

### 🔍 Advanced Search & Filtering
- Full-text search across title, content, author
- Filter by tags, author, date range
- Sort by date, views, title
- Pagination support

### 👤 User Profiles
- Extended user profiles
- Avatar uploads
- Bio, location, website fields
- User statistics (articles, comments count)
- Public profile pages

### 📊 API Documentation
- Auto-generated Swagger/OpenAPI docs
- Interactive API testing interface
- Comprehensive endpoint descriptions

### 🛡️ Security Features
- HTML content sanitization (XSS protection)
- CSRF protection
- CORS configuration
- Password validation
- SQL injection protection
- Secure JWT implementation

## 🛠️ Technology Stack

- **Framework:** Django 5.0.6
- **API:** Django REST Framework 3.15.2
- **Authentication:** Simple JWT 5.3.1
- **Database:** PostgreSQL (production) / SQLite (development)
- **Image Processing:** Pillow 10.3.0
- **HTML Sanitization:** Bleach 6.1.0
- **API Documentation:** drf-spectacular 0.27.2
- **Filtering:** django-filter 24.3
- **CORS:** django-cors-headers 4.4.0

## 📦 Installation

### Prerequisites
- Python 3.10+
- PostgreSQL (optional, SQLite works too)
- pip and virtualenv

### Quick Start

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd blog-api