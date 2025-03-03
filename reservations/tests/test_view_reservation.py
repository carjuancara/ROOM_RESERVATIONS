import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from reservations.models import Reservation, Room, Clients
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Fixture para instancia de APIClient"""
    return APIClient()


@pytest.fixture
def auth_api_client(api_client, django_user_model):
    user = django_user_model.objects.create_user(
        username="testuser", password="testpass")
    refresh = RefreshToken.for_user(user)
    api_client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {str(refresh.access_token)}')
    return api_client


@pytest.fixture
def new_reservation():
    """Fixture para crear una habitacion"""
    client = Clients.objects.create(
        name="Juan",
        lastname="Perez",
        email="juan.perez@example.com",
        document_number="1234567890",
        street="Calle Falsa 123",
        city="Madrid",
        state="Madrid",
        country="España",
        phone="+34600123456"
    )

    # creamos una habitacion para los test
    room = Room.objects.create(
        number=1,
        type='single',
        price_for_night=100.24,
        is_reserved=False,
        status='available',
        description='descripcion de la habitacion',
        capacity=4,
        amenities={'wifi': True, 'air_conditioning': True, 'minibar': False,
                   'jacuzzi': False, 'tv': True, 'breakfast_included': True}

    )

    # Creamos una reserva para ese cliente
    reservation = Reservation.objects.create(
        date_in="2025-01-01",
        date_out="2025-01-05",
        status="pending",
        total_price=500.00,
        client=client,  # Relación con el cliente
        room_id=room.id,  # Suponiendo que ya tienes una habitación con ID 1
        created_at=datetime.now(),  # Asignar el valor de la fecha de creación
        updated_at=datetime.now(),
    )

    return reservation


class TestReservationView:
    def test_create_reservation(self, api_client, new_reservation):
        new_reservation.status == status.HTTP_201_CREATED

    def test_verify_data_return(self, auth_api_client, new_reservation):
        api_url = reverse('reservations:reservation-list')

        response = auth_api_client.get(api_url, format="json")
        # Asegurar que la respuesta es exitosa
        assert response.status_code == 200, f"Error: {response.json()}"

        resp = response.json()
        print('response', resp)

        assert resp[0]["date_in"] == "2025-01-01"
        assert resp[0]["date_out"] == "2025-01-05"
        assert resp[0]["status"] == "pending"
        assert resp[0]["total_price"] == "500.00"
