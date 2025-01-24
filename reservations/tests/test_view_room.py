import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Room

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Fixture para instancia de APIClient"""
    return APIClient()


@pytest.fixture
def new_room(db):
    """Fixture para crear una habitacion"""
    return {
        "number": 101,
        "type": "double",
        "price_for_night": 120.00,
        "is_reserved": False,
        "status": "available",
        "description": "A spacious double room with a view.",
        "capacity": 2,
        "amenities": {
                "wifi": True,
                "air_conditioning": True,
                "minibar": False,
                "jacuzzi": False,
                "tv": True,
                "breakfast_included": True
        }
    }


class TestRoomView:
    def test_create_room(self, api_client, new_room):

        api_url = reverse('reservations:room-list')
        response = api_client.post(api_url, new_room, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_verify_data_return(self, api_client, new_room):
        api_url = reverse('reservations:room-list')

        api_client.post(api_url, new_room, format="json")
        response = api_client.get(api_url, format="json")

        room = response.json()

        assert room[0]["number"] == 101
        assert room[0]["type"] == "double"
        assert room[0]["price_for_night"] == "120.00"
        assert room[0]["is_reserved"] == False
        assert room[0]["status"] == "available"
        assert room[0]["description"] == "A spacious double room with a view."
        assert room[0]["capacity"] == 2
        assert room[0]["amenities"] == {
            "wifi": True,
            "air_conditioning": True,
            "minibar": False,
            "jacuzzi": False,
            "tv": True,
            "breakfast_included": True
        }
