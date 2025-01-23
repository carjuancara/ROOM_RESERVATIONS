from rest_framework import serializers
from .models import Clients, Room, Reservation


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = ['name', 'lastname', 'document_number', 'street',
                  'city', 'state', 'country', 'email', 'phone']
        read_only_fields = ('created_at', )


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['date_in', 'date_out', 'status', 'total_price']
        read_only_fields = ('created_at', 'updated_at')
