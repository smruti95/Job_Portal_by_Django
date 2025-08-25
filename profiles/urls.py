from django.urls import path
from .views import ProfileAPIView, ExperienceAPIView, EducationAPIView

urlpatterns = [
    path("profile/", ProfileAPIView.as_view(), name="profile"),
    path("experience/", ExperienceAPIView.as_view(), name="add-experience"),
    path("experience/<uuid:pk>/", ExperienceAPIView.as_view(), name="update-delete-experience"),
    path("education/", EducationAPIView.as_view(), name="add-education"),
    path("education/<uuid:pk>/", EducationAPIView.as_view(), name="update-delete-education"),
]
