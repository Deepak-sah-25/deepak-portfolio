import time
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.cache import cache
from .models import Profile, SkillCategory, Skill, Project, Experience, Education, Service, ContactMessage
from .forms import ContactForm


def get_client_ip(request):
    """Safely determine client IP through proxy / load balancer (Render, Railway, Cloudflare)."""
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0].strip()
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip or "127.0.0.1"


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
    client_ip = get_client_ip(request)

    # 1. IP Cooldown (Anti-Spam Flood Protection: 25 seconds between messages)
    cooldown_key = f"contact_cooldown_{client_ip}"
    if cache.get(cooldown_key):
        return JsonResponse(
            {
                "success": False,
                "message": "You are submitting too fast. Please wait 25 seconds before sending another message.",
            },
            status=429,
        )

    # 2. Hourly Quota (Maximum 5 messages per hour per IP)
    hourly_key = f"contact_hourly_{client_ip}"
    hourly_count = cache.get(hourly_key, 0)
    if hourly_count >= 5:
        return JsonResponse(
            {
                "success": False,
                "message": "You have reached the maximum message limit for this hour. For urgent queries, please WhatsApp Deepak directly (+977 9829014425).",
            },
            status=429,
        )

    # 3. Session Cooldown Fallback
    last_submit = request.session.get("last_contact_submit_time", 0)
    current_time = time.time()
    if current_time - last_submit < 20:
        return JsonResponse(
            {
                "success": False,
                "message": "Please wait a few moments before submitting another message.",
            },
            status=429,
        )

    form = ContactForm(request.POST)
    if form.is_valid():
        contact_message = form.save()
        request.session["last_contact_submit_time"] = current_time

        # Set 25-second cooldown and increment hourly count
        cache.set(cooldown_key, True, 25)
        cache.set(hourly_key, hourly_count + 1, 3600)

        # Print alert directly to terminal / Render server logs immediately
        print(
            f"\n{'='*55}\n📩 [NEW CONTACT MESSAGE RECEIVED ON PORTFOLIO]\nFrom: {contact_message.name} <{contact_message.email}>\nSubject: {contact_message.subject or 'No Subject'}\nMessage:\n{contact_message.message}\n{'='*55}\n",
            flush=True,
        )

        # 1. Send Email Alert (Supports Resend HTTPS API for Render free tier + Django SMTP)
        try:
            import json
            import urllib.request
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
            recipient = getattr(settings, "CONTACT_NOTIFICATION_EMAIL", "deepakraj90054@gmail.com")

            # Check for Resend API Key (Bypasses Render's port 587 block, 100% free)
            import os
            resend_key = (getattr(settings, "RESEND_API_KEY", "") or os.environ.get("RESEND_API_KEY", "")).strip()
            if resend_key:
                print(f"[Email Notification] Sending via Resend API to {recipient}...", flush=True)
                resend_payload = json.dumps({
                    "from": "Deepak Portfolio <onboarding@resend.dev>",
                    "to": [recipient],
                    "subject": email_subject,
                    "text": email_body,
                }).encode("utf-8")
                req = urllib.request.Request(
                    "https://api.resend.com/emails",
                    data=resend_payload,
                    headers={
                        "Authorization": f"Bearer {resend_key}",
                        "Content-Type": "application/json",
                        "User-Agent": "Mozilla/5.0",
                    },
                )
                with urllib.request.urlopen(req, timeout=8) as response:
                    print(f"[Email Notification] Resend API SUCCESS: {response.read().decode('utf-8')}", flush=True)
            else:
                print("[Email Notification Warning] RESEND_API_KEY is NOT set in Render Environment variables! Attempting SMTP fallback...", flush=True)
                # Fallback to standard Django SMTP (Local PC or Open SMTP ports)
                from django.core.mail import send_mail
                send_mail(
                    subject=email_subject,
                    message=email_body,
                    from_email=getattr(settings, "DEFAULT_FROM_EMAIL", "noreply@deepaksah.com.np"),
                    recipient_list=[recipient],
                    fail_silently=True,
                )
        except Exception as e:
            print(f"[Email Notification Error] {e}", flush=True)
            if hasattr(e, "read"):
                try:
                    print(f"[Email Notification Error Detail] {e.read().decode('utf-8')}", flush=True)
                except Exception:
                    pass

        # 2. Automated WhatsApp alert via CallMeBot (if API key is set)
        try:
            from django.conf import settings
            import urllib.request
            import urllib.parse

            callmebot_key = getattr(settings, "CALLMEBOT_APIKEY", "")
            callmebot_phone = getattr(settings, "CALLMEBOT_PHONE", "9779829014425")
            if callmebot_key and callmebot_phone:
                wa_alert_text = (
                    f"🔔 *New Portfolio Message!*\n"
                    f"*From:* {contact_message.name}\n"
                    f"*Email:* {contact_message.email}\n"
                    f"*Subject:* {contact_message.subject or 'None'}\n\n"
                    f"*Message:*\n{contact_message.message}"
                )
                encoded_text = urllib.parse.quote(wa_alert_text)
                api_url = f"https://api.callmebot.com/whatsapp.php?phone={callmebot_phone}&text={encoded_text}&apikey={callmebot_key}"
                req = urllib.request.Request(api_url, headers={"User-Agent": "Mozilla/5.0"})
                urllib.request.urlopen(req, timeout=4)
        except Exception:
            pass

        # 3. Optional Instant Telegram Alert (Free & 100% reliable on Render)
        try:
            from django.conf import settings
            import urllib.request
            import urllib.parse

            tg_token = getattr(settings, "TELEGRAM_BOT_TOKEN", "")
            tg_chat_id = getattr(settings, "TELEGRAM_CHAT_ID", "")
            if tg_token and tg_chat_id:
                tg_msg = (
                    f"🔔 *New Portfolio Inquiry*\n\n"
                    f"👤 *Name:* {contact_message.name}\n"
                    f"📧 *Email:* {contact_message.email}\n"
                    f"📝 *Subject:* {contact_message.subject or 'N/A'}\n\n"
                    f"💬 *Message:*\n{contact_message.message}"
                )
                tg_url = f"https://api.telegram.org/bot{tg_token}/sendMessage"
                tg_payload = urllib.parse.urlencode({"chat_id": tg_chat_id, "text": tg_msg, "parse_mode": "Markdown"}).encode("utf-8")
                tg_req = urllib.request.Request(tg_url, data=tg_payload, headers={"User-Agent": "Mozilla/5.0"})
                urllib.request.urlopen(tg_req, timeout=4)
        except Exception:
            pass

        # Create direct prefilled WhatsApp URL for the client/sender
        import urllib.parse
        wa_followup = (
            f"Hi Deepak, I just submitted an inquiry on your portfolio website!\n\n"
            f"Name: {contact_message.name}\n"
            f"Subject: {contact_message.subject or 'Project Scope'}\n"
            f"Message: {contact_message.message}"
        )
        prefilled_wa_url = f"https://wa.me/9779829014425?text={urllib.parse.quote(wa_followup)}"

        return JsonResponse(
            {
                "success": True,
                "message": f"Thank you, {contact_message.name}! Your message has been sent successfully.",
                "whatsapp_url": prefilled_wa_url,
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
