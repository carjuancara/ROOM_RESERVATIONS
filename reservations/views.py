from rest_framework import viewsets, status
from django.contrib.auth.models import User
from reservations.models import Clients, Room, Reservation
from reservations.serializers import ClientSerializer, RoomSerializer, ReservationSerializer, UserSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
from rest_framework.response import Response


class RegisterUser(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Clients.objects.all()
    serializer_class = ClientSerializer


class RoomViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    queryset = Room.objects.all()
    serializer_class = RoomSerializer

    # Solo los administradores pueden crear o eliminar habitaciones
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        """
        Permisos diferenciados según el tipo de acción
        """
        if self.action in ['create', 'destroy', 'update', 'partial_update']:
            # Solo admin puede crear, eliminar o modificar reservaciones
            permission_classes = [IsAdminUser]
        else:
            # Consultas y listados requieren solo autenticación
            permission_classes = [IsAuthenticated]

        return [permission() for permission in permission_classes]

    def list(self, request):
        """
        Listar reservaciones (solo usuarios autenticados)
        """
        # Filtrar reservaciones según el usuario
        if request.user.is_staff:
            # Admins ven todas las reservaciones
            queryset = Reservation.objects.all()
        else:
            # Usuarios normales ven solo sus propias reservaciones
            try:
                client = Clients.objects.get(user=request.user)
                queryset = Reservation.objects.filter(client=client)
            except Clients.DoesNotExist:
                queryset = Reservation.objects.none()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        """
        Detalle de reservación (solo usuarios autenticados)
        """
        reservation = self.get_object()

        # Verificar si el usuario tiene permiso para ver esta reservación
        if not request.user.is_staff:
            try:
                client = Clients.objects.get(user=request.user)
                if reservation.client != client:
                    return Response(
                        {"detail": "No tiene permiso para ver esta reservación"},
                        status=status.HTTP_403_FORBIDDEN
                    )
            except Clients.DoesNotExist:
                return Response(
                    {"detail": "No tiene permiso para ver esta reservación"},
                    status=status.HTTP_403_FORBIDDEN
                )

        serializer = self.get_serializer(reservation)
        return Response(serializer.data)

    @action(detail=False, methods=['GET'], permission_classes=[IsAuthenticated])
    def my_reservations(self, request):
        """
        Acción personalizada para ver reservaciones del usuario actual
        """
        try:
            client = Clients.objects.get(user=request.user)
            queryset = Reservation.objects.filter(client=client)
        except Clients.DoesNotExist:
            queryset = Reservation.objects.none()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
