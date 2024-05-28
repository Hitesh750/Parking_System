from django.db import models

class ParkingLot(models.Model):
    id = models.CharField(max_length=10, primary_key=True, default='PR1234')

class Floor(models.Model):
    parking_lot = models.ForeignKey(ParkingLot, on_delete=models.CASCADE)
    number = models.IntegerField()

class Slot(models.Model):
    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('truck', 'Truck')
    ]

    floor = models.ForeignKey(Floor, on_delete=models.CASCADE)
    number = models.IntegerField()
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    is_occupied = models.BooleanField(default=False)

class Vehicle(models.Model):
    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('bike', 'Bike'),
        ('truck', 'Truck')
    ]

    type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    registration_number = models.CharField(max_length=20)
    color = models.CharField(max_length=20)

class Ticket(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)
    vehicle = models.OneToOneField(Vehicle, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
