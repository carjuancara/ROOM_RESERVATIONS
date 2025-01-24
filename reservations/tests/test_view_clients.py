import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import Clients, Room, Reservation

pytestmark = pytest.mark.django_db


@pytest.fixture
def api_client():
    """Fixture para instancia de APIClient"""
    return APIClient()


@pytest.fixture
def new_client(db):
    """Fixture para crear un usuario"""
    return {
        "name": "testuser",
        "lastname": "test lastuser",
        "email": "test@example.com",
        "document_number": 545874580,
        "street": "san miguel 123",
        "city": "lules",
        "state": "state_street",
        "country": "country1"}


class TestClientView:
    def test_create_client(self, api_client, new_client):

        api_url = reverse('reservations:client-list')
        response = api_client.post(api_url, new_client, format="json")
        assert response.status_code == status.HTTP_201_CREATED

    def test_verify_data_return(self, api_client, new_client):
        api_url = reverse('reservations:client-list')

        api_client.post(api_url, new_client, format="json")
        response = api_client.get(api_url, format="json")

        client = response.json()
        print(client[0])
        assert client[0]["lastname"] == "test lastuser"
        assert client[0]["email"] == "test@example.com"
        assert client[0]["document_number"] == "545874580"
