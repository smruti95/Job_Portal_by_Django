from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status,filters
from django.shortcuts import get_object_or_404
from .models import Company
from .serializers import CompanySerializer
from django_filters.rest_framework import DjangoFilterBackend
from job_portal.pagination import SetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
class CompanyListCreateView(APIView):
    companies = Company.objects.all()
    serializer_class = CompanySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["name", "location", "industry"] 
    search_fields = ["name", "description"] 
    ordering_fields = ["created_at", "name"]  
    ordering = ["-created_at"]
    pagination_class = SetPagination
    @swagger_auto_schema(
        operation_summary="List all companies",
        responses={200: CompanySerializer(many=True)},
        security=[{"Bearer": []}]
    )
    def get(self, request):
        companies = Company.objects.all()
        paginator = self.pagination_class()
        paginated_companies = paginator.paginate_queryset(companies, request)
        serializer = CompanySerializer(paginated_companies, many=True)
        return paginator.get_paginated_response(serializer.data)

    @swagger_auto_schema(
        operation_summary="Create a new company",
        request_body=CompanySerializer,
        responses={201: CompanySerializer},
        security=[{"Bearer": []}]
    )
    def post(self, request):
        serializer = CompanySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CompanyDetailView(APIView):
    @swagger_auto_schema(
        operation_summary="Retrieve a company",
        responses={200: CompanySerializer},
        security=[{"Bearer": []}]
    )
    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Update a company",
        request_body=CompanySerializer,
        responses={200: CompanySerializer},
        security=[{"Bearer": []}]
    )
    def put(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Partially update a company",
        request_body=CompanySerializer,
        responses={200: CompanySerializer},
        security=[{"Bearer": []}]
    )
    def patch(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        operation_summary="Retrieve a company",
        responses={200: CompanySerializer},
        security=[{"Bearer": []}]
    )
    def get(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_summary="Delete a company",
        responses={204: openapi.Response("No Content")},
        security=[{"Bearer": []}]
    )
    def delete(self, request, pk):
        company = get_object_or_404(Company, pk=pk)
        company.delete()
        return Response({"message": "Company deleted"}, status=status.HTTP_204_NO_CONTENT)
