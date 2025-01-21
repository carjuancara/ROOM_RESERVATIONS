from reservations.models import Clients
from django.core.exceptions import ValidationError


import pytest


@pytest.fixture
def new_client():
    # Crear un usuario en la base de datos de prueba
    return Clients.objects.create(
        name="Juan Ignacio",
        lastname="Perez",
        document_number="d5846795122",
        street="España 246",
        city="Barcelona",
        state="Barcelona",
        country="España",
        email="juanignacio@email.com",
        phone="+30382145897",
    )


@pytest.mark.django_db
class TestClients:
    def test_create_client(self, new_client):
        """
        Verificar que el usuario se creó correctamente
        """

        assert Clients.objects.count() == 1

    def test_verify_client_data(self, new_client):
        """
        Verificar que el cliente tiene datos con longitudes válidas
        """
        client = Clients.objects.get(id=new_client.id)

        # Diccionario de campos y sus longitudes máximas
        field_lengths = {
            "name": 50,
            "lastname": 50,
            "document_number": 15,
            "street": 100,
            "city": 50,
            "state": 50,
            "country": 50,
        }

        for field, max_length in field_lengths.items():
            value = getattr(client, field)
        assert len(value) <= max_length, f"El campo '{
            field}' excede la longitud máxima de {max_length}"

    def test_verify_type_data(self, new_client):
        """
        verifica que los datos son del tipo correcto
        """

        client = Clients.objects.get(id=new_client.id)
        assert type(client.name) is str
        assert type(client.lastname) is str
        assert type(client.document_number) is str
        assert type(client.street) is str
        assert type(client.city) is str
        assert type(client.state) is str
        assert type(client.country) is str

    def test_email_must_be_unique(self, new_client):
        """
        Verifica que el correo electrónico no esté repetido
        """
        # Crear un nuevo cliente con el mismo email que el cliente existente
        duplicate_client = Clients(
            name="Juan",
            lastname="Perez",
            email=new_client.email,  # Mismo email que el cliente existente
            phone="+30382145897"
        )

        # Se espera que la validación falle debido a la restricción de unicidad
        with pytest.raises(ValidationError, match="El email debe ser único."):
            duplicate_client.full_clean()
