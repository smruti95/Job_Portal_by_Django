from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import Profile, Experience, Education
from .serializers import ProfileSerializer, ExperienceSerializer, EducationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from job_portal.pagination import SetPagination
from profiles.utils import send_mail
from django.conf import settings
from django.db import transaction
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class ProfileAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated,filters.SearchFilter, filters.OrderingFilter]
    users = Profile.objects.all()
    serializer_class = ProfileSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["user", "bio", "location"]
    search_fields = ["user__username", "bio", "location"]
    ordering_fields = ["created_at", "user__username"]
    ordering = ["-created_at"]
    pagination_class = SetPagination
    @swagger_auto_schema(
        operation_summary="Retrieve user profile",
        responses={200: ProfileSerializer},
        security=[{"Bearer": []}]
    )

    def get(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="Create a new user profile",
        request_body=ProfileSerializer,
        responses={201: ProfileSerializer},
        security=[{"Bearer": []}]
    )

    def post(self, request):
        if hasattr(request.user, "profile"):
            return Response(
                {"error": "Profile already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ProfileSerializer(data=request.data)
        if serializer.is_valid():
            try:
                with transaction.atomic():
                    profile = serializer.save(user=request.user)
                    transaction.on_commit(lambda: send_mail(
                        subject="Profile Created Successfully",
                        message=f"Hello {request.user.email}, your profile has been created.",
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[request.user.email],
                        fail_silently=False,
                    ))
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Update user profile",
        request_body=ProfileSerializer,
        responses={200: ProfileSerializer},
        security=[{"Bearer": []}]
    )
    def put(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Delete user profile",
        responses={204: 'No Content'},
        security=[{"Bearer": []}]
    )

    def delete(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        profile.delete()
        return Response({"message": "Profile deleted"}, status=status.HTTP_204_NO_CONTENT)
class ExperienceAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new experience",
        request_body=ExperienceSerializer,
        responses={201: ExperienceSerializer},
        security=[{"Bearer": []}]
    )
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = ExperienceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Update an experience",
        request_body=ExperienceSerializer,
        responses={200: ExperienceSerializer},
        security=[{"Bearer": []}]
    )
    def put(self, request, pk):
        profile = get_object_or_404(Profile, user=request.user)
        experience = get_object_or_404(Experience, pk=pk, profile=profile)
        serializer = ExperienceSerializer(experience, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Delete an experience",
        responses={204: 'No Content'},
        security=[{"Bearer": []}]
    )

    def delete(self, request, pk):
        profile = get_object_or_404(Profile, user=request.user)
        experience = get_object_or_404(Experience, pk=pk, profile=profile)
        experience.delete()
        return Response({"message": "Experience deleted"}, status=status.HTTP_204_NO_CONTENT)

class EducationAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Create a new education",
        request_body=EducationSerializer,
        responses={201: EducationSerializer},
        security=[{"Bearer": []}]
    )
    def post(self, request):
        profile = get_object_or_404(Profile, user=request.user)
        serializer = EducationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Update an education",
        request_body=EducationSerializer,
        responses={200: EducationSerializer},
        security=[{"Bearer": []}]
    )
    def put(self, request, pk):
        profile = get_object_or_404(Profile, user=request.user)
        education = get_object_or_404(Education, pk=pk, profile=profile)
        serializer = EducationSerializer(education, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Delete an education",
        responses={204: 'No Content'},
        security=[{"Bearer": []}]
    )

    def delete(self, request, pk):
        profile = get_object_or_404(Profile, user=request.user)
        education = get_object_or_404(Education, pk=pk, profile=profile)
        education.delete()
        return Response({"message": "Education deleted"}, status=status.HTTP_204_NO_CONTENT)
