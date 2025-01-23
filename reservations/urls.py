from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ClientViewSet, RoomViewSet, ReservationViewSet

router = DefaultRouter()
router.register(r'client', ClientViewSet)
router.register(r'room', RoomViewSet)
router.register(r'reservation', ReservationViewSet)

urlpatterns = [
    path('', include(router.urls))
]
