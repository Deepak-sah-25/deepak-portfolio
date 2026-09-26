from django.contrib import admin
from .models import (
    Profile,
    SkillCategory,
    Skill,
    Project,
    Experience,
    Service,
    ContactMessage,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "short_title", "current_company", "location", "is_active")
    fieldsets = (
        (
            "Personal Information",
            {
                "fields": (
                    "name",
                    "short_title",
                    "extended_title",
                    "current_role",
                    "current_company",
                    "location",
                )
            },
        ),
        (
            "Taglines & Biography",
            {
                "fields": (
                    "hero_tagline",
                    "alternative_tagline",
                    "bio_intro",
                    "bio_extended",
                    "career_goal",
                )
            },
        ),
        (
            "Contact & Social Links",
            {
                "fields": (
                    "email",
                    "phone",
                    "whatsapp_number",
                    "github_url",
                    "linkedin_url",
                )
            },
        ),
        (
            "Assets & Status",
            {
                "fields": (
                    "profile_image",
                    "resume_file",
                    "is_active",
                )
            },
        ),
    )


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 1


@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "order")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SkillInline]


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "proficiency", "icon_name", "is_featured", "order")
    list_filter = ("category", "is_featured")
    search_fields = ("name",)
    list_editable = ("proficiency", "is_featured", "order")


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "project_type", "role", "order", "is_featured")
    list_filter = ("is_featured", "project_type")
    search_fields = ("title", "technologies", "description")
    prepopulated_fields = {"slug": ("title",)}
    list_editable = ("order", "is_featured")


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("role", "company", "period", "is_current", "order")
    list_editable = ("order", "is_current")
    search_fields = ("role", "company", "technologies")


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)
    search_fields = ("title", "description")


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "subject", "created_at", "is_read")
    list_filter = ("is_read", "created_at")
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "subject", "message", "created_at")
    list_editable = ("is_read",)
