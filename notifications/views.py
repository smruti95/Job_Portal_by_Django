from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.utils import timezone
from .models import Notification
from .serializers import NotificationSerializer
from rest_framework import status, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from job_portal.pagination import SetPagination
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class NotificationListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ["is_read", "created_at"]
    pagination_class = SetPagination
    search_fields = ["message"]
    ordering_fields = ["created_at"]
    ordering = ["-created_at"]
    @swagger_auto_schema(
        operation_summary="List all notifications",
        responses={200: NotificationSerializer(many=True)},
        security=[{"Bearer": []}]
    )

    def get(self, request):
        is_read = request.query_params.get("is_read", None)
        qs = Notification.objects.filter(recipient=request.user).order_by("-created_at")
        if is_read is not None:
            qs = qs.filter(is_read=is_read.lower() == "true")
        serializer = NotificationSerializer(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    @swagger_auto_schema(
        operation_summary="Create a new notification",
        request_body=NotificationSerializer,
        responses={201: NotificationSerializer},
        security=[{"Bearer": []}]
    )

    def post(self, request):
        data = request.data.copy()
        if "recipient" not in data:
            data["recipient"] = request.user.id
        serializer = NotificationSerializer(data=data)
        if serializer.is_valid():
            notification = serializer.save()
            return Response(NotificationSerializer(notification).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotificationDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    @swagger_auto_schema(
        operation_summary="Retrieve a notification",
        responses={200: NotificationSerializer},
        security=[{"Bearer": []}]
    )
    def get_object(self, pk, user):
        try:
            return Notification.objects.get(pk=pk, recipient=user)
        except Notification.DoesNotExist:
            return None

    def get(self, request, pk):
        notification = self.get_object(pk, request.user)
        if not notification:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = NotificationSerializer(notification)
        return Response(serializer.data)
    @swagger_auto_schema(
        operation_summary="Update a notification",
        request_body=NotificationSerializer,
        responses={200: NotificationSerializer},
        security=[{"Bearer": []}]
    )
    def put(self, request, pk):
        notification = self.get_object(pk, request.user)
        if not notification:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NotificationSerializer(notification, data=request.data)
        if serializer.is_valid():
            notification = serializer.save()
            return Response(NotificationSerializer(notification).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @swagger_auto_schema(
        operation_summary="Delete a notification",
        responses={204: 'No Content'},
        security=[{"Bearer": []}]
    )

    def delete(self, request, pk):
        notification = self.get_object(pk, request.user)
        if not notification:
            return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)
        notification.delete()
        return Response({"message": "Notification deleted"}, status=status.HTTP_204_NO_CONTENT)
