
import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from reservations.models import Room
from django.contrib.auth import get_user_model

User = get_user_model()

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Fixture para instancia de APIClient"""
    return APIClient()


@pytest.fixture
def new_room():
    """Fixture para crear una habitación"""
    room = Room.objects.create(
        number=101,
        type='single',
        price_for_night=100.24,
        is_reserved=False,
        status='available',
        description='Descripción de la habitación',
        capacity=4,
        amenities={'wifi': True, 'air_conditioning': True, 'minibar': False,
                   'jacuzzi': False, 'tv': True, 'breakfast_included': True}
    )
    return room


@pytest.fixture
def authenticated_api_client(api_client):
    """Fixture para obtener un cliente API autenticado con JWT"""
    user = User.objects.create_user(
        username='testuser', password='testpass123')

    # Obtener el token JWT
    url = reverse('token_obtain_pair')
    response = api_client.post(
        url, {'username': 'testuser', 'password': 'testpass123'}, format='json')

    assert response.status_code == status.HTTP_200_OK, f"Error al obtener token JWT: {response.data}"
    assert 'access' in response.data, "No se encontró el token de acceso en la respuesta"

    token = response.data['access']

    # Configurar el token en las cabeceras
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
    return api_client


class TestRoomView:
    def test_create_room(self, authenticated_api_client):
        url = reverse('reservations:room-list')

        data = {
            "number": 102,
            "type": "double",
            "price_for_night": "150.50",
            "is_reserved": False,
            "status": "available",
            "description": "Habitación doble con vistas al mar",
            "capacity": 2,
            "amenities": {
                "wifi": True,
                "air_conditioning": True,
                "minibar": True,
                "jacuzzi": True,
                "tv": True,
                "breakfast_included": True
            }
        }

        response = authenticated_api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED, f"Error: {response.json()}"

        # Verificar que se creó la habitación
        assert Room.objects.filter(number=102).exists()

    def test_verify_data_return(self, authenticated_api_client, new_room):
        api_url = reverse('reservations:room-list')

        # Verificar que la habitación existe antes de hacer la solicitud
        assert Room.objects.exists(
        ), "No hay habitaciones en la base de datos antes de ejecutar el test."

        response = authenticated_api_client.get(api_url, format="json")
        assert response.status_code == status.HTTP_200_OK, f"Error al obtener habitaciones: {response.data}"

        resp = response.json()

        # Comprobar si la respuesta es una lista o está paginada
        if isinstance(resp, dict) and 'results' in resp:
            # Si está paginada, obtener results
            results = resp['results']
        else:
            # Si es una lista directa
            results = resp

        assert len(
            results) > 0, "La API no devolvió datos. Revisa si la base de datos tiene habitaciones."

        # Buscar la habitación creada en el fixture
        room_found = False
        for room in results:
            if room["number"] == 101:
                assert room["type"] == "single"
                assert room["price_for_night"] == "100.24"
                room_found = True
                break

        assert room_found, "No se encontró la habitación creada en la respuesta"
