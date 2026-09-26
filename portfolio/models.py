from django.db import models


class Profile(models.Model):
    name = models.CharField(max_length=150, default="Deepak Sah Kanu")
    short_title = models.CharField(max_length=150, default="Django Developer")
    extended_title = models.CharField(
        max_length=200, default="Django Developer | Full-Stack Web Developer"
    )
    hero_tagline = models.CharField(
        max_length=255,
        default="Building modern, scalable web applications with Django.",
    )
    alternative_tagline = models.CharField(
        max_length=255,
        default="Turning ideas into reliable, scalable web applications.",
    )
    bio_intro = models.TextField(
        default=(
            "I am Deepak Sah Kanu, a Django Developer and Full-Stack Web Developer focused on building modern, "
            "scalable, secure, and user-friendly web applications. I primarily work with Python and Django on the backend "
            "and HTML, CSS, JavaScript, and Bootstrap on the frontend."
        )
    )
    bio_extended = models.TextField(
        default=(
            "I enjoy transforming real-world requirements into clean, practical, and maintainable web applications. "
            "My development interests include healthcare systems, service-booking platforms, REST APIs, authentication, "
            "authorization, database-driven applications, and multi-tenant systems."
        )
    )
    career_goal = models.TextField(
        default=(
            "My goal is to grow as a professional Django / Full-Stack Developer and work on scalable real-world software systems. "
            "I specialize in advanced Django development, REST API architecture, scalable backend systems, PostgreSQL, and multi-tenant SaaS applications."
        )
    )
    current_company = models.CharField(max_length=150, default="Anjan lab company")
    current_role = models.CharField(max_length=150, default="Django Developer")
    location = models.CharField(max_length=100, default="Nepal")
    email = models.CharField(max_length=150, default="deepakraj90054@email.com", blank=True)
    phone = models.CharField(max_length=50, blank=True, default="+977 9829014425")
    whatsapp_number = models.CharField(max_length=50, blank=True, default="+977 9829014425")
    github_url = models.CharField(max_length=255, blank=True, default="https://github.com/Deepak-sah-25")
    linkedin_url = models.CharField(max_length=255, blank=True, default="https://linkedin.com")
    resume_file = models.FileField(upload_to="resumes/", blank=True, null=True)
    profile_image = models.FileField(upload_to="profile/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    @property
    def whatsapp_url(self):
        clean = "".join([c for c in (self.whatsapp_number or self.phone) if c.isdigit()])
        if clean and not clean.startswith("977") and len(clean) == 10:
            clean = "977" + clean
        return f"https://wa.me/{clean}" if clean else ""

    class Meta:
        verbose_name = "Personal Profile"
        verbose_name_plural = "Personal Profiles"

    def __str__(self):
        return f"{self.name} ({self.short_title})"


class SkillCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Skill Category"
        verbose_name_plural = "Skill Categories"

    def __str__(self):
        return self.name


class Skill(models.Model):
    category = models.ForeignKey(
        SkillCategory, related_name="skills", on_delete=models.CASCADE
    )
    name = models.CharField(max_length=100)
    proficiency = models.PositiveIntegerField(
        default=90, help_text="Proficiency percentage between 1 and 100"
    )
    icon_name = models.CharField(
        max_length=50,
        default="code",
        help_text="Name of icon (e.g. python, django, database, server, frontend, git, layers)",
    )
    is_featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "Skill"
        verbose_name_plural = "Skills"

    def __str__(self):
        return f"{self.name} ({self.proficiency}%)"


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    project_type = models.CharField(
        max_length=150,
        help_text="e.g. Healthcare / Hospital Management System",
    )
    role = models.CharField(max_length=150, default="Django Developer")
    summary = models.TextField(
        help_text="Concise summary displayed on project cards"
    )
    description = models.TextField(
        help_text="Detailed overview of technical architecture and concepts"
    )
    key_features = models.TextField(
        help_text="List key features separated by newlines"
    )
    technologies = models.CharField(
        max_length=255,
        help_text="Comma-separated technologies (e.g. Python, Django, DRF, PostgreSQL)",
    )
    live_url = models.URLField(blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    image = models.FileField(upload_to="projects/", blank=True, null=True)
    badge = models.CharField(max_length=50, blank=True, default="Featured")
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Project"
        verbose_name_plural = "Projects"

    def __str__(self):
        return self.title

    def get_features_list(self):
        return [f.strip() for f in self.key_features.split("\n") if f.strip()]

    def get_tech_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]


class Experience(models.Model):
    company = models.CharField(max_length=150)
    role = models.CharField(max_length=150)
    location = models.CharField(max_length=100, default="Nepal")
    period = models.CharField(max_length=100, default="Present")
    is_current = models.BooleanField(default=True)
    responsibilities = models.TextField(
        help_text="Key responsibilities separated by newlines"
    )
    technologies = models.CharField(
        max_length=255,
        help_text="Comma-separated technologies used",
        blank=True,
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "Work Experience"
        verbose_name_plural = "Work Experiences"

    def __str__(self):
        return f"{self.role} at {self.company}"

    def get_responsibilities_list(self):
        return [r.strip() for r in self.responsibilities.split("\n") if r.strip()]

    def get_tech_list(self):
        return [t.strip() for t in self.technologies.split(",") if t.strip()]


class Service(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon = models.CharField(
        max_length=50,
        default="server",
        help_text="Icon identifier (e.g. server, api, tenant, database)",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "title"]
        verbose_name = "Service"
        verbose_name_plural = "Services"

    def __str__(self):
        return self.title


class ContactMessage(models.Model):
    name = models.CharField(max_length=150)
    email = models.EmailField()
    subject = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Contact Message"
        verbose_name_plural = "Contact Messages"

    def __str__(self):
        return f"Message from {self.name} ({self.email}) - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
