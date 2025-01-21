import pytest
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
