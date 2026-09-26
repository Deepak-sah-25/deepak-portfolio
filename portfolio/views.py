from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Profile, SkillCategory, Skill, Project, Experience, Service, ContactMessage
from .forms import ContactForm


def index_view(request):
    profile = Profile.objects.filter(is_active=True).first()
    if not profile:
        profile = Profile.objects.create()

    categories = SkillCategory.objects.prefetch_related("skills").all()
    featured_skills = Skill.objects.filter(is_featured=True)[:8]
    projects = Project.objects.all()
    experiences = Experience.objects.all()
    services = Service.objects.all()
    contact_form = ContactForm()

    context = {
        "profile": profile,
        "categories": categories,
        "featured_skills": featured_skills,
        "projects": projects,
        "experiences": experiences,
        "services": services,
        "contact_form": contact_form,
    }
    return render(request, "portfolio/index.html", context)


@require_POST
def contact_submit_view(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        contact_message = form.save()
        return JsonResponse(
            {
                "success": True,
                "message": f"Thank you, {contact_message.name}! Your message has been sent successfully. Deepak will get back to you shortly.",
            }
        )
    else:
        errors = [f"{field}: {', '.join(errs)}" for field, errs in form.errors.items()]
        return JsonResponse(
            {
                "success": False,
                "message": "Please correct the errors in the form.",
                "errors": errors,
            },
            status=400,
        )


def project_detail_api(request, pk):
    project = get_object_or_404(Project, pk=pk)
    return JsonResponse(
        {
            "id": project.pk,
            "title": project.title,
            "project_type": project.project_type,
            "role": project.role,
            "summary": project.summary,
            "description": project.description,
            "features": project.get_features_list(),
            "technologies": project.get_tech_list(),
            "live_url": project.live_url or "",
            "github_url": project.github_url or "",
            "image_url": project.image.url if project.image else "",
        }
    )
