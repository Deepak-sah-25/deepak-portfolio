from django.core.management.base import BaseCommand
from portfolio.models import (
    Profile,
    SkillCategory,
    Skill,
    Project,
    Experience,
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
        profile.extended_title = "Django Developer | Full-Stack Web Developer"
        profile.hero_tagline = "Building modern, scalable web applications with Django."
        profile.alternative_tagline = "Turning ideas into reliable, scalable web applications."
        profile.bio_intro = (
            "I am Deepak Sah Kanu, a Django Developer and Full-Stack Web Developer focused on building modern, "
            "scalable, secure, and user-friendly web applications. I primarily work with Python and Django on the backend "
            "and HTML, CSS, JavaScript, and Bootstrap on the frontend."
        )
        profile.bio_extended = (
            "I enjoy transforming real-world requirements into clean, practical, and maintainable web applications. "
            "My development interests include healthcare systems, service-booking platforms, REST APIs, authentication, "
            "authorization, database-driven applications, and multi-tenant systems."
        )
        profile.career_goal = (
            "My goal is to grow as a professional Django / Full-Stack Developer and work on scalable real-world software systems. "
            "I specialize in advanced Django development, REST API architecture, scalable backend systems, PostgreSQL, and multi-tenant SaaS applications."
        )
        profile.current_company = "Anjan lab company"
        profile.current_role = "Django Developer"
        profile.location = "Nepal"
        profile.email = "deepak.developer@example.com"
        profile.phone = "+977 (Nepal)"
        profile.github_url = "https://github.com"
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
                    ("Django", 95, "django"),
                    ("Django REST Framework", 92, "api"),
                    ("REST APIs", 90, "server"),
                    ("Django ORM", 92, "database"),
                    ("Authentication & Permissions", 90, "shield"),
                    ("Custom User Models", 88, "users"),
                    ("Class-Based & Function Views", 90, "code"),
                    ("Middleware & Service-Layer", 85, "layers"),
                ],
            },
            {
                "category": "Programming Languages",
                "slug": "programming-languages",
                "order": 2,
                "skills": [
                    ("Python", 94, "python"),
                    ("JavaScript", 85, "javascript"),
                    ("HTML5", 95, "html"),
                    ("CSS3", 90, "css"),
                ],
            },
            {
                "category": "Database & Multi-Tenancy",
                "slug": "database-multi-tenancy",
                "order": 3,
                "skills": [
                    ("PostgreSQL", 90, "database"),
                    ("django-tenants", 92, "layers"),
                    ("PostgreSQL Schemas", 90, "server"),
                    ("Multi-Tenant Architecture", 88, "building"),
                    ("Tenant Data Isolation", 90, "shield"),
                    ("Query Optimization & Modeling", 86, "activity"),
                ],
            },
            {
                "category": "Frontend Development",
                "slug": "frontend-development",
                "order": 4,
                "skills": [
                    ("Bootstrap", 90, "layout"),
                    ("Responsive Web Design", 92, "smartphone"),
                    ("Django Template Language", 94, "file-code"),
                    ("Interactive UI Components", 85, "sparkles"),
                ],
            },
            {
                "category": "Tools & Practices",
                "slug": "tools-practices",
                "order": 5,
                "skills": [
                    ("Git & GitHub", 90, "git"),
                    ("Linux / Ubuntu / Terminal", 88, "terminal"),
                    ("Clean Code & Modular Architecture", 90, "check-circle"),
                    ("API Testing & Debugging", 88, "bug"),
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

        # 3. Work Experience (Anjan lab company)
        exp, _ = Experience.objects.get_or_create(
            company="Anjan lab company",
            role="Django Developer",
            defaults={"location": "Nepal", "period": "Present (Active Role)", "is_current": True},
        )
        exp.location = "Nepal"
        exp.period = "Current"
        exp.is_current = True
        exp.responsibilities = (
            "Django backend development and business logic implementation\n"
            "REST API development and integration using Django REST Framework\n"
            "Database-driven application development with PostgreSQL\n"
            "Authentication, role-based authorization, and permission enforcement\n"
            "Appointment management and patient-related hospital modules\n"
            "Hospital management workflows optimization and data integrity\n"
            "API testing, debugging, and backend architecture maintenance\n"
            "Production-oriented development and continuous code refactoring\n"
            "Git and GitHub based collaborative branching and pull request workflow"
        )
        exp.technologies = "Python, Django, Django REST Framework, PostgreSQL, JavaScript, Git, Linux"
        exp.order = 1
        exp.save()
        self.stdout.write(self.style.SUCCESS("✓ Work Experience configured"))

        # 4. Projects
        projects_data = [
            {
                "title": "Anjan Hospital Management System",
                "slug": "anjan-hospital-management-system",
                "project_type": "Healthcare / Hospital Management System",
                "role": "Django Developer",
                "badge": "Healthcare SaaS",
                "summary": "Comprehensive hospital management and patient workflow platform with appointment scheduling, multi-tenant isolation, and secure REST APIs.",
                "description": (
                    "Engineered a production-oriented healthcare and hospital management system designed to streamline clinical "
                    "operations, medical appointments, and patient care workflows. Built with a robust Django and Django REST Framework backend "
                    "interfacing with PostgreSQL, ensuring strict data security, role-based access control, and high-reliability data operations."
                ),
                "key_features": (
                    "Patient record management and medical history tracking\n"
                    "Automated doctor appointment scheduling and status updates\n"
                    "Role-based authentication & permissions (Doctors, Staff, Patients, Admins)\n"
                    "RESTful APIs for seamless client-side and external system communication\n"
                    "Hospital operational workflows and departmental data handling\n"
                    "Multi-tenant database architecture and PostgreSQL schema isolation\n"
                    "Rigorous API testing, exception handling, and audit trails"
                ),
                "technologies": "Python, Django, Django REST Framework, PostgreSQL, JavaScript, HTML, CSS",
                "order": 1,
            },
            {
                "title": "Sadi Sewa — Wedding Service Booking Platform",
                "slug": "sadi-sewa-wedding-booking-platform",
                "project_type": "Wedding / Event Service Booking Platform",
                "role": "Full-Stack Django Developer",
                "badge": "Full-Stack Platform",
                "summary": "Multi-vendor wedding and event booking marketplace featuring verified vendors, date-based reservations, cart management, and customer accounts.",
                "description": (
                    "Developed a complete end-to-end event and wedding service booking platform connecting customers with vetted service vendors. "
                    "Covers discovery, multi-service cart management, scheduling, vendor verification, and pricing models across event categories "
                    "such as Wedding Decoration, Catering, Photography, Car Booking, and Event Planning."
                ),
                "key_features": (
                    "Dual-role authentication for Customer and Vendor accounts\n"
                    "Vendor profile management with verified credentials\n"
                    "Multi-category service listings (Decoration, Catering, Photography, Car Booking)\n"
                    "Dynamic pricing models, promotional discounts, and verified customer ratings\n"
                    "Add to Cart system supporting multiple simultaneous service reservations\n"
                    "Date-based service availability checking and booking calendar\n"
                    "Customer dashboard with reservation status tracking and order history\n"
                    "Responsive mobile-first user interface built with Bootstrap and modern CSS"
                ),
                "technologies": "Python, Django, HTML, CSS, JavaScript, Bootstrap, PostgreSQL",
                "order": 2,
            },
            {
                "title": "Hospital Management / Multi-Tenant SaaS Development",
                "slug": "hospital-management-multi-tenant-saas",
                "project_type": "Multi-Tenant SaaS Architecture",
                "role": "Django Backend Developer",
                "badge": "Multi-Tenant Architecture",
                "summary": "Architectural implementation of multi-tenant SaaS architecture in Django using django-tenants and PostgreSQL schema-level isolation.",
                "description": (
                    "Deep exploration and production implementation of multi-tenancy in Django web applications. "
                    "Utilized django-tenants to provide complete schema-level database isolation on PostgreSQL, allowing multiple independent "
                    "hospitals or organizations to operate on a single shared codebase with guaranteed privacy and dedicated tenant subdomains."
                ),
                "key_features": (
                    "Multi-tenant data isolation using PostgreSQL schemas via django-tenants\n"
                    "Implementation of TenantMixin and DomainMixin models\n"
                    "Clear separation between shared applications and tenant-specific applications\n"
                    "Subdomain-driven tenant routing and context switching\n"
                    "Multi-tenant authentication and isolated user sessions\n"
                    "Tenant-aware database operations, migrations, and schema management\n"
                    "Scalable architecture designed for multi-client SaaS commercial deployment"
                ),
                "technologies": "Python, Django, django-tenants, PostgreSQL, SQL, Linux",
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

        # 5. Services
        services_data = [
            (
                "Django Backend & REST APIs",
                "Architecting high-performance backend systems, secure RESTful APIs with Django REST Framework, robust authentication, and business logic pipelines.",
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
                "Database Modeling & PostgreSQL",
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
