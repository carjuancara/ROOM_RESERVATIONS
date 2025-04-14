from django.contrib import admin
from reservations.models import Clients, Room, Reservation

# Register your models here.
admin.site.register(Clients)
admin.site.register(Room)
admin.site.register(Reservation)
