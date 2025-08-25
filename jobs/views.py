from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Job
from .serializers import JobSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from job_portal.pagination import SetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class JobListCreateView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    pagination_class = SetPagination
    filterset_fields = ["title", "company", "location", "is_active"]
    search_fields = ["title", "description"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]
    

    @swagger_auto_schema(
        operation_summary="List all jobs",
        responses={200: JobSerializer(many=True)},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        qs = Job.objects.all().order_by("-created_at")
        is_active = request.query_params.get("is_active")
        company = request.query_params.get("company")
        if is_active is not None:
            qs = qs.filter(is_active=is_active.lower() == "true")
        if company:
            qs = qs.filter(company_id=company)

        serializer = JobSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new job",
        request_body=JobSerializer,
        responses={201: JobSerializer},
        security=[{"Bearer": []}]
    )
    def post(self, request):
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            return Response(JobSerializer(job).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a job",
        responses={200: JobSerializer},
        security=[{"Bearer": []}]
    )
    def get_object(self, pk):
        try:
            return Job.objects.get(pk=pk)
        except Job.DoesNotExist:
            return None

    def get(self, request, pk):
        job = self.get_object(pk)
        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a job",
        request_body=JobSerializer,
        responses={200: JobSerializer},
        security=[{"Bearer": []}]
    )
    def put(self, request, pk):
        job = self.get_object(pk)
        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            job = serializer.save()
            return Response(JobSerializer(job).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Delete a job",
        responses={204: 'No Content'},
        security=[{"Bearer": []}]
    )


    def delete(self, request, pk):
        job = self.get_object(pk)
        if not job:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)

        job.delete()
        return Response({"message": "Job deleted"}, status=status.HTTP_204_NO_CONTENT)
