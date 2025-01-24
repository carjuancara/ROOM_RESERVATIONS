from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ClientViewSet, RoomViewSet, ReservationViewSet

app_name = "reservations"
router = DefaultRouter()
router.register(r'client', ClientViewSet, basename="client")
router.register(r'room', RoomViewSet, basename="room")
router.register(r'reservation', ReservationViewSet, basename="reservation")

urlpatterns = [
    path('', include(router.urls))
]
