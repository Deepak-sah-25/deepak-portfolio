import time
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Profile, SkillCategory, Skill, Project, Experience, Education, Service, ContactMessage
from .forms import ContactForm


def index_view(request):
    profile = Profile.objects.filter(is_active=True).first()
    if not profile:
        profile = Profile.objects.create()

    categories = SkillCategory.objects.prefetch_related("skills").all()
    featured_skills = Skill.objects.filter(is_featured=True)[:8]
    projects = Project.objects.all()
    experiences = Experience.objects.all()
    educations = Education.objects.all()
    services = Service.objects.all()
    contact_form = ContactForm()

    context = {
        "profile": profile,
        "categories": categories,
        "featured_skills": featured_skills,
        "projects": projects,
        "experiences": experiences,
        "educations": educations,
        "services": services,
        "contact_form": contact_form,
    }
    return render(request, "portfolio/index.html", context)


@require_POST
def contact_submit_view(request):
    # Cooldown flood protection: minimum 5 seconds between submissions
    last_submit = request.session.get("last_contact_submit_time", 0)
    current_time = time.time()
    if current_time - last_submit < 5:
        return JsonResponse(
            {
                "success": False,
                "message": "Please wait a few seconds before submitting another message.",
            },
            status=429,
        )

    form = ContactForm(request.POST)
    if form.is_valid():
        contact_message = form.save()
        request.session["last_contact_submit_time"] = current_time

        # Print alert directly to terminal running runserver
        print(f"\n{'='*55}\n📩 [NEW CONTACT MESSAGE RECEIVED ON PORTFOLIO]\nFrom: {contact_message.name} <{contact_message.email}>\nSubject: {contact_message.subject or 'No Subject'}\nMessage:\n{contact_message.message}\n{'='*55}\n")

        # Send email alert to Deepak if mail backend is configured
        try:
            from django.core.mail import send_mail
            from django.conf import settings

            email_subject = f"Portfolio Message from {contact_message.name}: {contact_message.subject or 'No Subject'}"
            email_body = (
                f"You received a new inquiry on your Deepak Sah Kanu Portfolio website!\n\n"
                f"Name: {contact_message.name}\n"
                f"Email: {contact_message.email}\n"
                f"Subject: {contact_message.subject or 'None'}\n"
                f"Message:\n{contact_message.message}\n\n"
                f"Quick reply by clicking: mailto:{contact_message.email}\n"
            )
            recipient = getattr(settings, "CONTACT_NOTIFICATION_EMAIL", "deepakraj90054@email.com")
            send_mail(
                subject=email_subject,
                message=email_body,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@deepaksah.com.np"),
                recipient_list=[recipient],
                fail_silently=True,
            )
        except Exception:
            pass

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


def download_resume_view(request):
    from django.conf import settings
    from django.http import FileResponse, HttpResponse

    profile = Profile.objects.filter(is_active=True).first()
    if profile and profile.resume_file:
        try:
            return FileResponse(
                profile.resume_file.open("rb"),
                as_attachment=True,
                filename=f"Resume_{profile.name.replace(' ', '_')}.pdf",
            )
        except Exception:
            pass

    default_resume = settings.BASE_DIR / "static" / "files" / "Deepak_Sah_Kanu_Resume.pdf"
    if default_resume.exists():
        return FileResponse(
            open(default_resume, "rb"),
            as_attachment=True,
            filename="Deepak_Sah_Kanu_Resume.pdf",
        )

    return HttpResponse(
        "Deepak's resume PDF will be attached soon via Django Admin! You can upload it in Django Admin > Profile > Resume file.",
        content_type="text/plain",
    )
