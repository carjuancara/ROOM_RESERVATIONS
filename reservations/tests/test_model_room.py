import pytest
from decimal import Decimal
from reservations.models import Room


@pytest.fixture
def new_room():
    return Room.objects.create(
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


@pytest.mark.django_db
class TestRoom:
    def test_create_room(self, new_room):
        """
        Verificar que la habitacion se creó correctamente
        """

        assert Room.objects.count() == 1

    def test_verify_room_data(self, new_room):
        """
        Verificar que la habitacion tiene datos con longitudes válidas
        """
        room = Room.objects.get(id=new_room.id)

        # Diccionario de campos y sus longitudes máximas
        field_lengths = {
            "type": 6,
            "status": 11,
        }

        for field, max_length in field_lengths.items():
            value = getattr(room, field)
        assert len(value) <= max_length, f"El campo '{
            field}' excede la longitud máxima de {max_length}"

    def test_verify_type_data(self, new_room):
        """
        verifica que los datos son del tipo correcto
        """

        room = Room.objects.get(id=new_room.id)
        assert type(room.number) is int
        assert type(room.type) is str
        assert type(room.is_reserved) is bool
        assert type(room.status) is str
        assert type(room.description) is str
        assert type(room.capacity) is int
        assert type(room.amenities) is dict
        assert type(room.price_for_night) is Decimal
