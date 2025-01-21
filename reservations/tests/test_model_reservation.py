import pytest
from reservations.models import Reservation, Clients, Room
from datetime import datetime


@pytest.fixture
def new_reservation():
    # Creamos un cliente
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


@pytest.mark.django_db
class TestReservation:
    def test_create_reservation(self, new_reservation):
        assert Reservation.objects.count() == 1

    def test_verify_data_with_valid_length(self, new_reservation):
        """
        Verificar que la RESERVACION tiene datos con longitudes válidas
        """
        reservation = Reservation.objects.get(id=new_reservation.id)

        # Diccionario de campos y sus longitudes máximas
        field_lengths = {
            "status": 9,
        }

        for field, max_length in field_lengths.items():
            value = getattr(reservation, field)
        assert len(value) <= max_length, f"El campo '{
            field}' excede la longitud máxima de {max_length}"
