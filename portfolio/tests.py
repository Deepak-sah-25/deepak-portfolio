from django.test import TestCase, Client
from django.urls import reverse
from django.core.cache import cache
from portfolio.models import (
    Profile,
    SkillCategory,
    Skill,
    Project,
    Experience,
    Education,
    Service,
    ContactMessage,
)


class PortfolioTests(TestCase):
    def setUp(self):
        cache.clear()
        self.client = Client()
        self.profile = Profile.objects.create(
            name="Deepak Sah Kanu",
            short_title="Django Developer",
            extended_title="Django Developer | Full-Stack Web Developer",
            hero_tagline="Building modern, scalable web applications with Django.",
            current_company="Anjan lab company",
            current_role="Django Developer",
            location="Nepal",
            is_active=True,
        )
        self.category = SkillCategory.objects.create(
            name="Backend Development",
            slug="backend-development",
            order=1,
        )
        self.skill = Skill.objects.create(
            category=self.category,
            name="Django",
            proficiency=95,
            icon_name="django",
            is_featured=True,
            order=1,
        )
        self.project = Project.objects.create(
            title="Anjan Hospital Management System",
            slug="anjan-hospital-management-system",
            project_type="Healthcare / Hospital Management System",
            role="Django Developer",
            summary="A comprehensive hospital management platform.",
            description="Detailed technical description of hospital architecture.",
            key_features="Appointment management\nPatient management\nMulti-tenant architecture",
            technologies="Python, Django, DRF, PostgreSQL",
            order=1,
            is_featured=True,
        )
        self.experience = Experience.objects.create(
            company="Anjan lab company",
            role="Django Developer",
            location="Nepal",
            period="Current",
            is_current=True,
            responsibilities="Django backend development\nREST API development",
            technologies="Python, Django, PostgreSQL",
        )
        self.service = Service.objects.create(
            title="Django Backend & REST APIs",
            description="Scalable backend architectures and APIs.",
            icon="server",
            order=1,
        )
        self.education = Education.objects.create(
            degree="Bachelor in Computer Application (BCA)",
            institution="Prime College",
            location="Kathmandu, Nepal",
            period="Running (3rd Year)",
            status="Bachelor Running 3rd Year",
            order=1,
        )

    def test_index_view_status_and_content(self):
        response = self.client.get(reverse("portfolio:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Deepak Sah Kanu")
        self.assertContains(response, "Anjan Hospital Management System")
        self.assertContains(response, "Anjan lab company")
        self.assertContains(response, "Technologies I Master")
        self.assertContains(response, "Prime College")
        self.assertContains(response, "Bachelor in Computer Application (BCA)")

    def test_contact_submit_valid(self):
        data = {
            "name": "Jane Doe",
            "email": "janedoe@example.com",
            "subject": "Django Project Inquiry",
            "message": "Hi Deepak, we would like to collaborate on a Django healthcare project.",
        }
        response = self.client.post(reverse("portfolio:contact_submit"), data)
        self.assertEqual(response.status_code, 200)
        res_json = response.json()
        self.assertTrue(res_json["success"])
        self.assertIn("Thank you, Jane Doe!", res_json["message"])
        self.assertTrue(ContactMessage.objects.filter(email="janedoe@example.com").exists())

    def test_contact_submit_invalid(self):
        data = {
            "name": "",
            "email": "not-an-email",
            "message": "",
        }
        response = self.client.post(reverse("portfolio:contact_submit"), data)
        self.assertEqual(response.status_code, 400)
        res_json = response.json()
        self.assertFalse(res_json["success"])

    def test_project_detail_api(self):
        response = self.client.get(
            reverse("portfolio:project_detail_api", kwargs={"pk": self.project.pk})
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["title"], "Anjan Hospital Management System")
        self.assertEqual(len(data["features"]), 3)
        self.assertIn("Multi-tenant architecture", data["features"])
        self.assertIn("Python", data["technologies"])

    def test_models_str_and_helpers(self):
        self.assertEqual(str(self.profile), "Deepak Sah Kanu (Django Developer)")
        self.assertEqual(str(self.category), "Backend Development")
        self.assertEqual(str(self.skill), "Django (95%)")
        self.assertEqual(str(self.project), "Anjan Hospital Management System")
        self.assertEqual(str(self.experience), "Django Developer at Anjan lab company")
        self.assertEqual(str(self.education), "Bachelor in Computer Application (BCA) - Prime College (Running (3rd Year))")
        self.assertEqual(str(self.service), "Django Backend & REST APIs")
        self.assertEqual(len(self.project.get_features_list()), 3)
        self.assertEqual(len(self.project.get_tech_list()), 4)

    def test_download_resume_view(self):
        response = self.client.get(reverse("portfolio:download_resume"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")

    def test_sitemap_xml(self):
        response = self.client.get("/sitemap.xml")
        self.assertEqual(response.status_code, 200)
        self.assertIn("xml", response["Content-Type"])
        self.assertContains(response, "<urlset")
        self.assertContains(response, "<loc>")

    def test_robots_txt(self):
        response = self.client.get("/robots.txt")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/plain")
        self.assertContains(response, "User-agent: *")
        self.assertContains(response, "Sitemap:")

    def test_seo_meta_and_structured_data(self):
        response = self.client.get(reverse("portfolio:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<script type="application/ld+json">')
        self.assertContains(response, '"@type": "Person"')
        self.assertContains(response, "canonical")
        self.assertContains(response, "og:site_name")
        self.assertContains(response, "twitter:card")

    def test_contact_honeypot_spam_protection(self):
        # Automated bot filling honeypot should be blocked
        data = {
            "name": "Bot Spammer",
            "email": "bot@spam.com",
            "subject": "Spam Offer",
            "message": "Spam text message buy now",
            "hp_company": "Bot Trap Triggered",
        }
        response = self.client.post(reverse("portfolio:contact_submit"), data)
        self.assertEqual(response.status_code, 400)
        json_data = response.json()
        self.assertFalse(json_data["success"])
        self.assertIn("Spam submission detected.", json_data["errors"][0])

    def test_contact_rate_limit_flood_protection(self):
        # First submission succeeds
        data = {
            "name": "Legit User",
            "email": "legit@example.com",
            "subject": "Hello",
            "message": "First message",
            "hp_company": "",
        }
        res1 = self.client.post(reverse("portfolio:contact_submit"), data)
        self.assertEqual(res1.status_code, 200)

        # Second submission immediately from same session is rate-limited (429)
        res2 = self.client.post(reverse("portfolio:contact_submit"), data)
        self.assertEqual(res2.status_code, 429)
        self.assertFalse(res2.json()["success"])

    def test_resume_aliases(self):
        self.assertEqual(self.client.get("/download-resume/").status_code, 200)
        self.assertEqual(self.client.get("/resume/").status_code, 200)

