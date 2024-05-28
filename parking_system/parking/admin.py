from django.contrib import admin
from .models import ParkingLot, Floor, Slot, Vehicle, Ticket



class ParkingLotAdmin(admin.ModelAdmin):
    list_display = ('id')

class FloorAdmin(admin.ModelAdmin):
    list_display = ('parking_lot', 'number')

class SlotAdmin(admin.ModelAdmin):
    list_display = ('floor', 'number', 'vehicle_type', 'is_occupied')

class VehicleAdmin(admin.ModelAdmin):
    list_display = ('type', 'registration_number','color')

class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'slot', 'vehicle', 'created_at')
    
admin.site.register(ParkingLot)
admin.site.register(Floor)
admin.site.register(Slot)
admin.site.register(Vehicle)
admin.site.register(Ticket)