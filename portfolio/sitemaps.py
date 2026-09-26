from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Profile, Project


class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 1.0

    def items(self):
        return ["portfolio:index", "portfolio:download_resume"]

    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return Project.objects.filter(is_featured=True)

    def location(self, item):
        # Anchor link on homepage
        return f"{reverse('portfolio:index')}#projects"
