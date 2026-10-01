import shutil
from django.conf import settings
from django.core.management.base import BaseCommand
from portfolio.models import (
    Profile,
    SkillCategory,
    Skill,
    Project,
    Experience,
    Education,
    Service,
)


class Command(BaseCommand):
    help = "Seed database with Deepak Sah Kanu's exact portfolio profile and project data."

    def _sync_media_assets(self):
        """Ensure media directories exist and sync essential logos/profile images from static."""
        media_profile_dir = settings.MEDIA_ROOT / "profile"
        media_projects_dir = settings.MEDIA_ROOT / "projects"
        media_profile_dir.mkdir(parents=True, exist_ok=True)
        media_projects_dir.mkdir(parents=True, exist_ok=True)

        # Profile image sync
        static_profile_img = settings.BASE_DIR / "static" / "images" / "deepak.jpg"
        media_profile_img = media_profile_dir / "deepak.jpg"
        if static_profile_img.exists():
            shutil.copy2(static_profile_img, media_profile_img)

        # Project logos sync
        project_logos = [
            "starnews_logo.png",
            "kinaun_brand.svg",
            "batomechanic_logo.png",
            "cdc_logo.png",
        ]
        for logo in project_logos:
            static_logo = settings.BASE_DIR / "static" / "images" / logo
            media_logo = media_projects_dir / logo
            if static_logo.exists():
                shutil.copy2(static_logo, media_logo)

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Deepak Sah Kanu's portfolio data..."))

        # Synchronize media assets from static assets for fresh deployments
        self._sync_media_assets()

        # 1. Profile
        profile, created = Profile.objects.get_or_create(id=1)
        profile.name = "Deepak Sah Kanu"
        profile.short_title = "Django Developer"
        profile.extended_title = "Full-Stack Django Developer | DRF & PostgreSQL"
        profile.hero_tagline = "Building modern, scalable web applications with Django."
        profile.alternative_tagline = "Turning ideas into reliable, scalable web applications."
        profile.bio_intro = (
            "Results-driven Full-Stack Django Developer with over 2 years of experience in designing, "
            "building, and deploying scalable web applications and RESTful APIs. Specializes in Python, "
            "Django REST Framework (DRF), PostgreSQL, and multi-tenant SaaS architectures."
        )
        profile.bio_extended = (
            "Proven track record of developing robust backend systems, optimizing database performance, "
            "and delivering secure, user-friendly solutions for the healthcare and e-commerce sectors. "
            "Experienced with asynchronous task processing using Redis & Celery, and containerized deployment with Docker."
        )
        profile.career_goal = (
            "My goal is to grow as a professional Django / Full-Stack Developer and work on scalable real-world software systems. "
            "I specialize in advanced Django development, REST API architecture, scalable backend systems, PostgreSQL, and multi-tenant SaaS applications."
        )
        profile.current_company = "Anjan Lab Company"
        profile.current_role = "Django Developer"
        profile.location = "Kathmandu, Lalitpur, Nepal"
        profile.email = "deepakraj90054@email.com"
        profile.phone = "+977 9829014425"
        profile.whatsapp_number = "+977 9829014425"
        profile.github_url = "https://github.com/Deepak-sah-25"
        profile.linkedin_url = "https://linkedin.com"
        profile.profile_image = "profile/deepak.jpg"
        profile.is_active = True
        profile.save()
        self.stdout.write(self.style.SUCCESS("✓ Profile configured"))

        # 2. Skill Categories and Skills
        skills_data = [
            {
                "category": "Backend Development",
                "slug": "backend-development",
                "order": 1,
                "skills": [
                    ("Python", 95, "python"),
                    ("Django", 95, "django"),
                    ("Django REST Framework", 92, "api"),
                    ("REST API Design", 92, "server"),
                    ("Django ORM", 92, "database"),
                    ("Authentication & Permissions", 90, "shield"),
                    ("Background Tasks (Celery & Redis)", 88, "activity"),
                    ("Service-Layer Architecture", 86, "layers"),
                ],
            },
            {
                "category": "Databases & Architecture",
                "slug": "databases-architecture",
                "order": 2,
                "skills": [
                    ("PostgreSQL", 92, "database"),
                    ("Multi-Tenant Architecture", 90, "building"),
                    ("django-tenants", 92, "layers"),
                    ("Schema Isolation", 90, "shield"),
                    ("Database Modeling & ORM", 90, "database"),
                    ("Query Optimization", 86, "activity"),
                ],
            },
            {
                "category": "Frontend Development",
                "slug": "frontend-development",
                "order": 3,
                "skills": [
                    ("HTML5", 95, "html"),
                    ("CSS3", 90, "css"),
                    ("JavaScript", 85, "javascript"),
                    ("Bootstrap", 90, "layout"),
                    ("Responsive Web Design", 92, "smartphone"),
                    ("Django Templates", 94, "file-code"),
                ],
            },
            {
                "category": "Tools & Technologies",
                "slug": "tools-technologies",
                "order": 4,
                "skills": [
                    ("Git & GitHub", 92, "git"),
                    ("Docker", 85, "server"),
                    ("Redis", 86, "database"),
                    ("Celery", 86, "activity"),
                    ("Linux / Ubuntu / Terminal", 88, "terminal"),
                    ("VS Code & AI Coding Tools", 90, "code"),
                    ("Clean Code & Modular Architecture", 90, "check-circle"),
                    ("Third-Party Integrations", 88, "sparkles"),
                ],
            },
        ]

        # Remove obsolete categories
        valid_slugs = [c["slug"] for c in skills_data]
        SkillCategory.objects.exclude(slug__in=valid_slugs).delete()

        for cat_info in skills_data:
            category, _ = SkillCategory.objects.get_or_create(
                slug=cat_info["slug"],
                defaults={"name": cat_info["category"], "order": cat_info["order"]},
            )
            category.name = cat_info["category"]
            category.order = cat_info["order"]
            category.save()

            # Remove obsolete skills in this category
            valid_skill_names = [s[0] for s in cat_info["skills"]]
            category.skills.exclude(name__in=valid_skill_names).delete()

            for idx, (skill_name, proficiency, icon) in enumerate(cat_info["skills"]):
                skill, _ = Skill.objects.get_or_create(
                    category=category,
                    name=skill_name,
                    defaults={
                        "proficiency": proficiency,
                        "icon_name": icon,
                        "order": idx + 1,
                        "is_featured": idx < 4,
                    },
                )
                skill.proficiency = proficiency
                skill.icon_name = icon
                skill.order = idx + 1
                skill.is_featured = idx < 4
                skill.save()

        self.stdout.write(self.style.SUCCESS("✓ Skills & Categories configured (clean & deduplicated)"))

        # 3. Work Experience
        exp_data = [
            {
                "company": "Anjan Lab Company",
                "role": "Django Developer",
                "location": "Nepal",
                "period": "August 2024 – Present",
                "is_current": True,
                "responsibilities": (
                    "Lead the backend development of secure, database-driven healthcare web applications using Django and Django REST Framework.\n"
                    "Architect and implement multi-tenant SaaS structures using PostgreSQL and django-tenants, ensuring strict schema isolation and data security across multiple hospital networks.\n"
                    "Build and maintain complex REST APIs for appointment management, patient workflows, and centralized clinical modules.\n"
                    "Optimize database queries and implement asynchronous task processing using Redis and Celery to improve application response times and performance.\n"
                    "Collaborate with cross-functional teams to refactor legacy codebases and streamline deployment workflows using Docker containerization."
                ),
                "technologies": "Python, Django, Django REST Framework, PostgreSQL, django-tenants, Redis, Celery, Docker, Linux",
                "order": 1,
            },
            {
                "company": "Independent Web Developer",
                "role": "Full-Stack Python Developer",
                "location": "Nepal",
                "period": "May 2024 – August 2024",
                "is_current": False,
                "responsibilities": (
                    "Designed and developed end-to-end web solutions for local businesses, focusing on backend logic, database management, and responsive frontend UI.\n"
                    "Created custom dashboards and data analytics tools, improving client operational efficiency."
                ),
                "technologies": "Python, Django, PostgreSQL, JavaScript, Bootstrap, HTML5, CSS3, Git",
                "order": 2,
            },
        ]

        for e_item in exp_data:
            exp, _ = Experience.objects.get_or_create(
                company=e_item["company"],
                role=e_item["role"],
                defaults={
                    "location": e_item["location"],
                    "period": e_item["period"],
                    "is_current": e_item["is_current"],
                    "order": e_item["order"],
                },
            )
            exp.location = e_item["location"]
            exp.period = e_item["period"]
            exp.is_current = e_item["is_current"]
            exp.responsibilities = e_item["responsibilities"]
            exp.technologies = e_item["technologies"]
            exp.order = e_item["order"]
            exp.save()

        self.stdout.write(self.style.SUCCESS("✓ Work Experiences configured"))

        # 4. Education
        edu, _ = Education.objects.get_or_create(
            degree="Bachelor in Computer Application (BCA)",
            institution="Prime College",
            defaults={
                "location": "Kathmandu, Nepal",
                "period": "Running (3rd Year)",
                "status": "Bachelor Running 3rd Year",
                "order": 1,
            },
        )
        edu.location = "Kathmandu, Nepal"
        edu.period = "Running (3rd Year)"
        edu.status = "Bachelor Running 3rd Year"
        edu.description = (
            "Undergraduate coursework in Computer Applications, Software Engineering, "
            "Data Structures & Algorithms, Database Management Systems (PostgreSQL/SQL), and Web Application Architecture."
        )
        edu.order = 1
        edu.save()
        self.stdout.write(self.style.SUCCESS("✓ Education configured"))

        # 5. Projects
        projects_data = [
            {
                "title": "Star News TV — Live Digital News & Media Portal",
                "slug": "star-news-tv-digital-media-portal",
                "project_type": "Live Digital News & Media Platform",
                "role": "Full-Stack Web Developer",
                "badge": "Live Production 🟢",
                "live_url": "https://www.starnewstv.com.np/",
                "summary": "High-traffic digital news and multimedia broadcasting platform in Nepal featuring breaking stories, category filtering, search, and responsive reader view.",
                "description": (
                    "Engineered and deployed a production-grade digital news and media broadcasting portal for Star News TV (https://www.starnewstv.com.np/). "
                    "Built with a high-performance backend supporting real-time news publishing, multimedia asset delivery, article categorization "
                    "(Politics, Entertainment, Sports, Society, Music), editorial author attribution, full-text search, and optimized database queries."
                ),
                "key_features": (
                    "Live production digital news portal serving active readers across Nepal\n"
                    "Dynamic breaking news banner & top-story multimedia carousel\n"
                    "Multi-category article filtering (Politics, Entertainment, Sports, Society, Music)\n"
                    "Keyword search with date-range filters and editorial author attribution\n"
                    "Optimized database schema and media asset delivery pipeline\n"
                    "SEO-optimized OpenGraph metadata, Twitter cards, and structured schema markup\n"
                    "100% responsive mobile-first UI with bilingual support"
                ),
                "technologies": "Python, Django, REST APIs, PostgreSQL, JavaScript, Next.js, Tailwind CSS",
                "image": "projects/starnews_logo.png",
                "order": 1,
            },
            {
                "title": "Kinaun — Multi-Vendor E-Commerce Platform",
                "slug": "kinaun-ecommerce-marketplace",
                "project_type": "Multi-Vendor E-Commerce Platform",
                "role": "Full-Stack Developer (Collaborative Team Project)",
                "badge": "Live Production 🟢",
                "live_url": "https://www.kinaun.com/",
                "summary": "Scalable multi-vendor online shopping marketplace and seller portal in Nepal built collaboratively with engineering team.",
                "description": (
                    "Collaborated with an agile engineering team to architect, build, and deploy Kinaun (https://www.kinaun.com/), "
                    "an active multi-vendor e-commerce marketplace in Nepal. Engineered seller onboarding and merchant administration dashboards, "
                    "catalog and inventory management, real-time customer order lifecycle tracking, checkout flows, and high-performance PostgreSQL relational schemas."
                ),
                "key_features": (
                    "Live production multi-vendor e-commerce platform in Nepal (kinaun.com)\n"
                    "Developed collaboratively in an agile cross-functional engineering team\n"
                    "Comprehensive seller center dashboard for store onboarding, analytics, and earnings reports\n"
                    "Product catalog management with category hierarchy and dynamic attribute filters\n"
                    "Real-time order lifecycle tracking, inventory sync, and customer checkout flows\n"
                    "Optimized PostgreSQL relational database architecture for high-volume transactions\n"
                    "Responsive mobile-first user interface tailored for seamless shopping and merchant management"
                ),
                "technologies": "Python, Django, PostgreSQL, REST APIs, JavaScript, Bootstrap, HTML5, CSS3",
                "image": "projects/kinaun_brand.svg",
                "order": 2,
            },
            {
                "title": "Bato Mechanic — Roadside Vehicle Assistance & Mechanic Platform",
                "slug": "bato-mechanic-roadside-assistance",
                "project_type": "On-Demand Automobile Assistance Platform",
                "role": "Full-Stack Web & API Developer",
                "badge": "Live Production 🟢",
                "live_url": "https://batomechanic.com/",
                "summary": "On-demand roadside assistance and vehicle mechanic booking platform in Nepal with emergency dispatch, repair catalogs, and REST APIs.",
                "description": (
                    "Engineered and deployed Bato Mechanic (https://batomechanic.com/), Nepal's premier digital platform connecting motorists "
                    "with certified mechanics during on-road vehicle breakdowns. Built robust backend RESTful APIs for real-time service requests, "
                    "emergency roadside dispatch, multi-category automobile repair catalog (bikes & cars), and multilingual content delivery."
                ),
                "key_features": (
                    "Live production roadside assistance platform operating across Nepal (batomechanic.com)\n"
                    "Real-time emergency mechanic dispatch and breakdown assistance request pipeline\n"
                    "Categorized vehicle maintenance and repair service catalog for bikes and cars\n"
                    "High-performance REST API backend supporting modern web and mobile clients\n"
                    "Bilingual localization system with dynamic English and Nepali language switching\n"
                    "Responsive modern UI architecture optimized for emergency mobile browser access"
                ),
                "technologies": "Python, Django, REST APIs, PostgreSQL, React, JavaScript, Tailwind CSS",
                "image": "projects/batomechanic_logo.png",
                "order": 3,
            },
            {
                "title": "CDC Cinemas — Movie Ticketing & Theater Management Portal",
                "slug": "cdc-cinemas-ticketing-portal",
                "project_type": "Entertainment & Movie Ticketing Platform",
                "role": "Full-Stack Web & Backend Developer",
                "badge": "Live Production 🟢",
                "live_url": "https://www.cdcnepal.com.np/",
                "summary": "Live cinema ticketing and theater management web portal in Kathmandu, Nepal featuring real-time showtimes, seat reservation, and payment processing.",
                "description": (
                    "Engineered and deployed the production web platform for CDC Cinemas (https://www.cdcnepal.com.np/), "
                    "a premier multiplex cinema in Kathmandu. Built dynamic seat selection systems, real-time showtime scheduling, "
                    "now showing & upcoming movie catalog management, automated ticket pricing matrices, and secure online payment workflows."
                ),
                "key_features": (
                    "Live production movie ticket booking portal operating in Kathmandu, Nepal (cdcnepal.com.np)\n"
                    "Dynamic now-showing and upcoming movie catalog with multimedia trailers and synopses\n"
                    "Interactive real-time seat reservation layout and showtime scheduling matrix\n"
                    "Tiered ticket rates, promotional discounts, and automated billing generation\n"
                    "Optimized database queries and media asset caching for high-traffic movie release days\n"
                    "Responsive modern UI architecture optimized for desktop and mobile moviegoers"
                ),
                "technologies": "Python, Django, PostgreSQL, REST APIs, JavaScript, Bulma CSS, HTML5",
                "image": "projects/cdc_logo.png",
                "order": 4,
            },
        ]

        # Clean up any obsolete/duplicate projects
        current_slugs = [p["slug"] for p in projects_data]
        deleted_count, _ = Project.objects.exclude(slug__in=current_slugs).delete()
        if deleted_count:
            self.stdout.write(self.style.WARNING(f"Cleaned up {deleted_count} obsolete/duplicate projects"))

        for p_data in projects_data:
            project, _ = Project.objects.get_or_create(
                slug=p_data["slug"],
                defaults={
                    "title": p_data["title"],
                    "project_type": p_data["project_type"],
                    "role": p_data["role"],
                    "badge": p_data["badge"],
                    "summary": p_data["summary"],
                    "description": p_data["description"],
                    "key_features": p_data["key_features"],
                    "technologies": p_data["technologies"],
                    "live_url": p_data.get("live_url"),
                    "order": p_data["order"],
                    "is_featured": True,
                },
            )
            project.title = p_data["title"]
            project.project_type = p_data["project_type"]
            project.role = p_data["role"]
            project.badge = p_data["badge"]
            project.summary = p_data["summary"]
            project.description = p_data["description"]
            project.key_features = p_data["key_features"]
            project.technologies = p_data["technologies"]
            project.live_url = p_data.get("live_url")
            if p_data.get("image"):
                project.image = p_data["image"]
            project.order = p_data["order"]
            project.is_featured = True
            project.save()

        self.stdout.write(self.style.SUCCESS("✓ Projects configured"))

        # 6. Services
        services_data = [
            (
                "Django Backend & REST APIs",
                "Architecting high-performance backend systems, secure RESTful APIs with Django REST Framework, robust authentication, and background task pipelines.",
                "server",
                1,
            ),
            (
                "Multi-Tenant SaaS Systems",
                "Designing and implementing multi-tenant architectures using django-tenants and PostgreSQL schemas with strict data isolation for SaaS platforms.",
                "layers",
                2,
            ),
            (
                "Full-Stack Web Development",
                "Building complete, production-ready web applications combining Django's powerful backend with responsive, mobile-first frontend interfaces.",
                "layout",
                3,
            ),
            (
                "Database Modeling & Optimization",
                "Designing optimized database relationships, schema migrations, complex ORM queries, and indexing strategies for scalable data-driven apps.",
                "database",
                4,
            ),
        ]

        for title, desc, icon, order in services_data:
            svc, _ = Service.objects.get_or_create(
                title=title,
                defaults={"description": desc, "icon": icon, "order": order},
            )
            svc.description = desc
            svc.icon = icon
            svc.order = order
            svc.save()

        self.stdout.write(self.style.SUCCESS("✓ Services configured"))
        self.stdout.write(self.style.SUCCESS("🎉 Successfully seeded all portfolio data for Deepak Sah Kanu!"))
