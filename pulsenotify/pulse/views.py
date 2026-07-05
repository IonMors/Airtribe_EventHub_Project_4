from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer
from django.shortcuts import get_object_or_404

from rest_framework.permissions import IsAuthenticated

from .models import PriceAlert

from .serializers import (
    RegisterSerializer,
    PriceAlertSerializer,
)
import random
from django.http import JsonResponse
from django.db.models import Count, Q
from rest_framework.permissions import IsAuthenticated

from .permissions import IsAdminUser
from .models import NotificationLog


class RegisterView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():

            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "username": user.username,
                    "access": str(refresh.access_token),
                    "role": user.profile.role
                },
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )


class LoginView(APIView):

    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(
            username=username,
            password=password
        )

        if user is None:
            return Response(
                {"error": "Invalid credentials"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken.for_user(user)

        return Response(
            {
                "access": str(refresh.access_token)
            },
            status=status.HTTP_200_OK
        )

class AlertListCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        alerts = PriceAlert.objects.filter(user=request.user)

        serializer = PriceAlertSerializer(
            alerts,
            many=True
        )

        return Response(serializer.data)

    def post(self, request):

        serializer = PriceAlertSerializer(
            data=request.data
        )

        if serializer.is_valid():

            serializer.save(
                user=request.user
            )

            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class AlertDeleteView(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, id):

        alert = get_object_or_404(
            PriceAlert,
            id=id
        )

        if alert.user != request.user:

            return Response(
                status=status.HTTP_404_NOT_FOUND
            )

        alert.status = PriceAlert.Status.INACTIVE

        alert.save()

        return Response(
            {
                "status": "inactive"
            }
        )

MOCK_PRICES = {
    "DEL-BOM": (3000, 7000),
    "BLR-HYD": (1500, 4000),
    "DEL-BLR": (4000, 9000),
    "BOM-GOA": (2000, 5000),
}


def get_flight_price(request):

    route = request.GET.get("route", "")

    price_range = MOCK_PRICES.get(route)

    if not price_range:
        return JsonResponse(
            {"error": "Route not found"},
            status=404
        )

    price = random.randint(*price_range)

    return JsonResponse({
        "route": route,
        "price": price
    })  

class AdminSummaryView(APIView):

    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):

        total_alerts = PriceAlert.objects.count()

        active_alerts = PriceAlert.objects.filter(
            status=PriceAlert.Status.ACTIVE
        ).count()

        triggered_alerts = PriceAlert.objects.filter(
            status=PriceAlert.Status.TRIGGERED
        ).count()

        total_notifications = NotificationLog.objects.count()

        top_routes = (
            PriceAlert.objects
            .values("origin", "destination")
            .annotate(alert_count=Count("id"))
            .order_by("-alert_count")
        )

        routes = []

        for route in top_routes:

            routes.append({

                "route": f"{route['origin']}-{route['destination']}",

                "alert_count": route["alert_count"]

            })

        return Response({

            "total_alerts": total_alerts,

            "active_alerts": active_alerts,

            "triggered_alerts": triggered_alerts,

            "total_notifications": total_notifications,

            "top_routes": routes

        })