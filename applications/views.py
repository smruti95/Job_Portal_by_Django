from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,filters
from django.shortcuts import get_object_or_404
from .models import Application
from .serializers import ApplicationSerializer
from django_filters.rest_framework import DjangoFilterBackend
from job_portal.pagination import SetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class ApplicationListCreateView(APIView):
    applications = Application.objects.all()
    serializer_class = ApplicationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["status", "job", "applicant"]  
    search_fields = ["cover_letter", "job__title", "applicant__email"]  
    ordering_fields = ["created_at", "status"] 
    ordering = ["-created_at"]
    pagination_class = SetPagination

    @swagger_auto_schema(
        operation_summary="Retrieve all applications",
        responses={200: ApplicationSerializer(many=True)},
        security=[{"Bearer": []}]
    )

    def get(self, request):
        applications = Application.objects.all()
        serializer = ApplicationSerializer(applications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Create a new application",
        request_body=ApplicationSerializer,
        responses={201: ApplicationSerializer},
        security=[{"Bearer": []}]
    )

    def post(self, request):
        serializer = ApplicationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve a specific application",
        responses={200: ApplicationSerializer},
        security=[{"Bearer": []}]
    )
    def get(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        serializer = ApplicationSerializer(application)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="Update a specific application",
        request_body=ApplicationSerializer,
        responses={200: ApplicationSerializer},
        security=[{"Bearer": []}]
    )
    def put(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        serializer = ApplicationSerializer(application, data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Partially update a specific application",
        request_body=ApplicationSerializer,
        responses={200: ApplicationSerializer},
        security=[{"Bearer": []}]
    )

    def patch(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Delete a specific application",
        responses={204: 'No Content'},
        security=[{"Bearer": []}]
    )

    def delete(self, request, pk):
        application = get_object_or_404(Application, pk=pk)
        application.delete()
        return Response({"detail": "Application deleted"}, status=status.HTTP_204_NO_CONTENT)
