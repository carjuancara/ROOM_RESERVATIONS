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
    email = models.EmailField(blank=True, unique=True, null=True)
    phone = PhoneNumberField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        super().clean()

        if self.email and Clients.objects.filter(email=self.email).exclude(id=self.id).exists():
            raise ValidationError({"email": "El email debe ser único."})

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
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    client = models.ForeignKey(
        Clients, on_delete=models.CASCADE, related_name='reservations')
    room = models.ForeignKey(
        Room, on_delete=models.CASCADE, related_name='reservations')

    def __str__(self):
        return self.status

    def clean(self):
        if self.date_out <= self.date_in:
            raise ValidationError(
                "The departure date must be after the arrival date.")

        # Verificar disponibilidad de la habitación
        overlapping_reservations = Reservation.objects.filter(
            room=self.room,
            date_in__lt=self.date_out,
            date_out__gt=self.date_in,
        ).exclude(id=self.id)

        if overlapping_reservations.exists():
            raise ValidationError(
                "The room is not available for the selected dates.")

        # Verificar capacidad
        if self.room.capacity < self.number_of_guests:  # Asumiendo que agregas un campo `number_of_guests`
            raise ValidationError(
                "The room does not have capacity for the number of guests.")
