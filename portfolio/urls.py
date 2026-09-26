from django.urls import path
from . import views

app_name = "portfolio"

urlpatterns = [
    path("", views.index_view, name="index"),
    path("contact/submit/", views.contact_submit_view, name="contact_submit"),
    path("api/projects/<int:pk>/", views.project_detail_api, name="project_detail_api"),
]
