from rest_framework import serializers
from reservations.models import Clients, Room, Reservation
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = [
            'name',
            'lastname',
            'document_number',
            'street',
            'country',
            'email',
            'phone'
        ]
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
