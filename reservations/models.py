from django.db import models
from django.core.exceptions import ValidationError
from phonenumber_field.modelfields import PhoneNumberField


class Clients(models.Model):
    name = models.CharField(max_length=50)
    lastname = models.CharField(max_length=50)
    document_number = models.CharField(max_length=15)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    email = models.EmailField(blank=True)
    phone = PhoneNumberField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


def validate_amenities(value):
    required_keys = {'wifi', 'air_conditioning',
                     'minibar', 'jacuzzi', 'tv', 'breakfast_included'}
    if not all(key in value for key in required_keys):
        raise ValidationError("Faltan claves requeridas en los amenities.")


class Room (models.Model):
    TYPE_ROOM = [
        ('single', 'Single'),
        ('double', 'Double'),
        ('twin', 'Twin'),
        ('suit', 'Suit'),
        ('deluxe', 'Deluxe')
    ]

    STATUS_ROOM = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('cleaning', 'Cleaning'),
        ('maintenance', 'Maintenance'),
    ]

    number = models.IntegerField()
    type = models.CharField(default='single', choices=TYPE_ROOM, max_length=6)
    price_for_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_reserved = models.BooleanField(default=False)
    status = models.CharField(
        default='available', choices=STATUS_ROOM, max_length=11)
    description = models.TextField(blank=True)
    capacity = models.IntegerField()
    amenities = models.JSONField(default=dict, validators=[validate_amenities])

    def __str__(self):
        return self.type


class Reservation(models.Model):
    STATUS_RESERVATION = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ]

    date_in = models.DateField()
    date_out = models.DateField()
    status = models.CharField(
        default='pending', choices=STATUS_RESERVATION, max_length=9)
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateField()
    updated_at = models.DateField()
    client = models.ForeignKey(
        Clients, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='Reservations')

    def __str__(self):
        return self.status
