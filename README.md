# 🚀 Deepak Sah Kanu — Developer Portfolio & Systems Showcase

A modern, high-performance personal portfolio website engineered with **Python**, **Django 6**, and **PostgreSQL**. Designed for recruiters, engineering managers, and clients to explore production projects, system architecture, technical skills, and download a verifiable ATS-friendly resume.

[![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Django](https://img.shields.io/badge/Django-6.1-092E20?style=flat&logo=django&logoColor=white)](https://www.djangoproject.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791?style=flat&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

---

## 🌟 Key Highlights & Features

- **⚡ Modern Dark Glassmorphism UI**: Mobile-first responsive layout with ambient glow gradients, interactive 3D card tilt, animated code terminals, and smooth navigation.
- **💼 Live Production Projects Showcase**:
  1. **[Star News TV](https://www.starnewstv.com.np/)**: Live digital news & multimedia broadcasting platform in Nepal.
  2. **[Kinaun](https://www.kinaun.com/)**: Multi-vendor e-commerce marketplace and merchant seller portal.
  3. **[Bato Mechanic](https://batomechanic.com/)**: On-demand emergency vehicle roadside assistance platform.
  4. **[CDC Cinemas](https://www.cdcnepal.com.np/)**: Multiplex movie ticketing and seat reservation portal.
- **📄 ATS Single-Page Resume Generator**: Built-in Python PDF engine (`generate_resume.py`) with photo embedding, verifiable credentials, and instant download via `/resume/download/`.
- **💬 Floating Speed Dial Contact Button**: Instant quick-connect channels for WhatsApp (`+977 9829014425`), direct email, phone call, and contact form scroll.
- **🛡️ Enterprise-Grade Security**:
  - Automated Bot Honeypot trap (`hp_company`) on contact form.
  - Session-based flood rate-limiting (`429 Too Many Requests`).
  - Strict CSRF validation, XSS auto-escaping, Clickjacking protection (`X_FRAME_OPTIONS = 'DENY'`).
  - HSTS, HTTPS redirection, and secure cookies for production.
- **🔍 SEO & Discoverability**:
  - Full Google Schema.org (`Person`, `WebSite`, `ProfilePage`) JSON-LD structured data.
  - Dynamic `sitemap.xml` and standard `robots.txt`.
  - OpenGraph and Twitter card preview metadata for social sharing.
- **☁️ Cloud Deployment Ready**: Complete setup with `build.sh`, `Procfile`, WhiteNoise static file compression, and environment variable configuration for Render, Railway, or VPS.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.12, Django 6.1.1, Django REST Framework (DRF)
- **Database**: PostgreSQL (Production) / SQLite3 (Local Dev) with `dj-database-url`
- **Frontend**: HTML5, Modern CSS3 (CSS Variables, Flexbox/Grid), JavaScript (Vanilla ES6+)
- **Production Server & Assets**: Gunicorn, WhiteNoise Compressed Static Storage
- **Architecture**: Multi-Tenant SaaS (django-tenants), REST APIs, Modular Service Layer

---

## 🚀 Quick Start (Local Development)

### 1. Clone the repository
```bash
git clone https://github.com/Deepak-sah-25/deepak-portfolio.git
cd deepak-portfolio
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv myenv
source myenv/bin/activate  # On Windows: myenv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run database migrations
```bash
python manage.py migrate
```

### 5. Seed Deepak's portfolio profile and projects
```bash
python manage.py seed_portfolio
```

### 6. Run the local development server
```bash
python manage.py runserver
```
Visit `http://127.0.0.1:8000/` in your browser.

---

## 🧪 Running Automated Tests

```bash
python manage.py test
```
All 12 automated unit tests cover:
- Profile and model helpers
- Skill categorization & deduplication
- Project detail APIs
- Contact form honeypot spam protection & rate limiting
- Resume download endpoints and aliases
- Sitemaps, robots.txt, and Schema.org structured data

---

## 🌐 Deploy to Render / Railway

This repository includes a production `build.sh` script:
1. Create a new **Web Service** on [Render.com](https://render.com/) or [Railway.app](https://railway.app/).
2. Connect your GitHub repository.
3. Set the **Build Command**: `./build.sh`
4. Set the **Start Command**: `gunicorn deepak_portfolio_website.wsgi:application`
5. Configure Environment Variables (see `.env.example`):
   - `SECRET_KEY`: Your secret key
   - `DEBUG`: `False`
   - `ALLOWED_HOSTS`: `*` or your custom domain
   - `CSRF_TRUSTED_ORIGINS`: `https://*.onrender.com`

---

## 📬 Contact & Connect

- **Name**: Deepak Sah Kanu
- **Role**: Full-Stack Django Developer | DRF & PostgreSQL
- **Location**: Kathmandu, Lalitpur, Nepal
- **Email**: [deepakraj90054@email.com](mailto:deepakraj90054@email.com)
- **WhatsApp / Phone**: [+977 9829014425](https://wa.me/9779829014425)
- **GitHub**: [github.com/Deepak-sah-25](https://github.com/Deepak-sah-25)

---
*Crafted with Python & Django • 2026*
