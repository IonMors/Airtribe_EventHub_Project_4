from django.urls import path

from .views import RegisterView, LoginView
from .views import (
    RegisterView,
    LoginView,
    AlertListCreateView,
    AlertDeleteView,
)
from .views import get_flight_price
from .views import AdminSummaryView

urlpatterns = [

    path(
        "auth/register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "auth/login/",
        LoginView.as_view(),
        name="login"
    ),

    path(
        "alerts/",
        AlertListCreateView.as_view(),
        name="alerts",
    ),

        path(
            "alerts/<int:id>/",
            AlertDeleteView.as_view(),
            name="delete-alert",
        ),
    path(
    "flights/price/",
    get_flight_price,
    name="flight-price",
),
    path(
    "admin/summary/",
    AdminSummaryView.as_view(),
),

]