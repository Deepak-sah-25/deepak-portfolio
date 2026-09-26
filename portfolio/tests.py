from django.test import TestCase, Client
from django.urls import reverse
from portfolio.models import (
    Profile,
    SkillCategory,
    Skill,
    Project,
    Experience,
    Service,
    ContactMessage,
)


class PortfolioTests(TestCase):
    def setUp(self):
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

    def test_index_view_status_and_content(self):
        response = self.client.get(reverse("portfolio:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Deepak Sah Kanu")
        self.assertContains(response, "Anjan Hospital Management System")
        self.assertContains(response, "Anjan lab company")
        self.assertContains(response, "Technologies I Master")

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
        self.assertEqual(str(self.service), "Django Backend & REST APIs")
        self.assertEqual(len(self.project.get_features_list()), 3)
        self.assertEqual(len(self.project.get_tech_list()), 4)

    def test_download_resume_view(self):
        response = self.client.get(reverse("portfolio:download_resume"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "application/pdf")
