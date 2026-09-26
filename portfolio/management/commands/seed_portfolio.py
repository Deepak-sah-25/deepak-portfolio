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

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Deepak Sah Kanu's portfolio data..."))

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
                    ("Third-Party Integrations", 88, "sparkles"),
                ],
            },
        ]

        for cat_info in skills_data:
            category, _ = SkillCategory.objects.get_or_create(
                slug=cat_info["slug"],
                defaults={"name": cat_info["category"], "order": cat_info["order"]},
            )
            category.name = cat_info["category"]
            category.order = cat_info["order"]
            category.save()

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

        self.stdout.write(self.style.SUCCESS("✓ Skills & Categories configured"))

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
                "title": "Anjan Hospital Management Information System (HMIS)",
                "slug": "anjan-hospital-management-system",
                "project_type": "Healthcare / Hospital Management System",
                "role": "Django Developer",
                "badge": "Healthcare SaaS",
                "summary": "Comprehensive clinical workflow platform tailored for the healthcare sector with multi-tenant configurations and REST APIs.",
                "description": (
                    "Architected a comprehensive clinical workflow platform tailored for the healthcare sector. "
                    "Developed secure multi-tenant hospital configurations, allowing separate medical facilities to operate independently on a unified backend. "
                    "Built dynamic REST API endpoints for patient registers, real-time appointment scheduling, and automated billing generation."
                ),
                "key_features": (
                    "Architected comprehensive clinical workflow platform tailored for healthcare\n"
                    "Secure multi-tenant hospital configurations with PostgreSQL schema isolation\n"
                    "Unified backend allowing independent medical facilities to operate securely\n"
                    "Dynamic REST API endpoints for patient registers and clinical logs\n"
                    "Real-time appointment scheduling and automated status tracking\n"
                    "Automated billing generation and hospital administration workflows"
                ),
                "technologies": "Python, Django, Django REST Framework, PostgreSQL, django-tenants, JavaScript, HTML, CSS",
                "order": 1,
            },
            {
                "title": "Sadi Sewa - Event & Wedding Booking Marketplace",
                "slug": "sadi-sewa-wedding-booking-platform",
                "project_type": "Wedding / Event Service Booking Platform",
                "role": "Full-Stack Django Developer",
                "badge": "Full-Stack Marketplace",
                "summary": "Scalable multi-vendor booking platform connecting users with wedding and event service providers.",
                "description": (
                    "Developed a scalable multi-vendor booking platform connecting users with wedding and event service providers. "
                    "Implemented comprehensive vendor profiles, dynamic service packaging, booking management systems, and secure payment architecture. "
                    "Designed an intuitive user interface utilizing Bootstrap and responsive HTML/CSS layouts."
                ),
                "key_features": (
                    "Scalable multi-vendor booking marketplace architecture\n"
                    "Comprehensive vendor profiles and verification workflows\n"
                    "Dynamic service packaging across decoration, catering, photography, and car rentals\n"
                    "Cart management system supporting multiple service reservations\n"
                    "Date-based service scheduling and booking availability check\n"
                    "Secure payment architecture and customer transaction history\n"
                    "Intuitive user interface utilizing Bootstrap and responsive layouts"
                ),
                "technologies": "Python, Django, PostgreSQL, HTML5, CSS3, JavaScript, Bootstrap",
                "order": 2,
            },
            {
                "title": "E-Commerce Seller Center Dashboard",
                "slug": "ecommerce-seller-center-dashboard",
                "project_type": "E-Commerce / Merchant Management Dashboard",
                "role": "Full-Stack Django Developer",
                "badge": "E-Commerce Dashboard",
                "summary": "Comprehensive seller dashboard featuring functionalities for seller registration, robust analytics, and earnings reports.",
                "description": (
                    "Engineered a comprehensive seller dashboard featuring functionalities for seller registration, robust analytics, and earnings reports. "
                    "Integrated real-time order tracking and status management using optimized PostgreSQL database relationships."
                ),
                "key_features": (
                    "Comprehensive seller registration, onboarding, and store profile management\n"
                    "Robust sales analytics and dynamic performance metrics dashboard\n"
                    "Automated earnings reports, payouts tracking, and revenue analytics\n"
                    "Real-time order tracking and lifecycle order status management\n"
                    "Optimized PostgreSQL database relationships and indexed query pipelines\n"
                    "Clean, modern responsive UI tailored for merchant workflow efficiency"
                ),
                "technologies": "Python, Django, PostgreSQL, JavaScript, Bootstrap, HTML5, CSS3",
                "order": 3,
            },
        ]

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
