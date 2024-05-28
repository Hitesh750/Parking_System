from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import ParkingLot, Floor, Slot, Vehicle, Ticket
from .serializers import ParkingLotSerializer, FloorSerializer, SlotSerializer, VehicleSerializer, TicketSerializer

class ParkingLotViewSet(viewsets.ModelViewSet):
    queryset = ParkingLot.objects.all()
    serializer_class = ParkingLotSerializer

    @action(detail=False, methods=['post'])
    def add_floor(self, request):
        parking_lot = ParkingLot.objects.get(id='PR1234')
        floor_number = request.data.get('number')
        floor = Floor.objects.create(parking_lot=parking_lot, number=floor_number)
        serializer = FloorSerializer(floor)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'])
    def add_slot(self, request):
        floor_number = request.data.get('floor_number')
        slot_number = request.data.get('slot_number')
        vehicle_type = request.data.get('vehicle_type')
        floor = Floor.objects.get(number=floor_number)
        slot = Slot.objects.create(floor=floor, number=slot_number, vehicle_type=vehicle_type)
        serializer = SlotSerializer(slot)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['post'] )
    def park_vehicle(self, request):
        vehicle_data = request.data.get('vehicle')
        vehicle_serializer = VehicleSerializer(data=vehicle_data)
        if vehicle_serializer.is_valid():
            vehicle = vehicle_serializer.save()
            slots = Slot.objects.filter(vehicle_type=vehicle.type, is_occupied=False).order_by('floor__number', 'number')
            if slots.exists():
                slot = slots.first()
                slot.is_occupied = True
                slot.save()
                ticket_id = f"PR1234_{slot.floor.number}_{slot.number}"
                ticket = Ticket.objects.create(id=ticket_id, slot=slot, vehicle=vehicle)
                ticket_serializer = TicketSerializer(ticket)
                return Response(ticket_serializer.data, status=status.HTTP_201_CREATED)
            return Response({'error': 'No available slots'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def unpark_vehicle(self, request):
        ticket_id = request.data.get('ticket_id')
        try:
            ticket = Ticket.objects.get(id=ticket_id)
            slot = ticket.slot
            slot.is_occupied = False
            slot.save()
            ticket.delete()
            ticket.vehicle.delete()
            return Response({'status': 'Vehicle unparked successfully'}, status=status.HTTP_200_OK)
        except Ticket.DoesNotExist:
            return Response({'error': 'Invalid ticket ID'}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def free_slots_count(self, request):
        vehicle_type = request.query_params.get('vehicle_type')
        floors = Floor.objects.all()
        result = {}
        for floor in floors:
            free_slots = Slot.objects.filter(floor=floor, vehicle_type=vehicle_type, is_occupied=False).count()
            result[f'Floor {floor.number}'] = free_slots
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def free_slots(self, request):
        vehicle_type = request.query_params.get('vehicle_type')
        floors = Floor.objects.all()
        result = {}
        for floor in floors:
            free_slots = Slot.objects.filter(floor=floor, vehicle_type=vehicle_type, is_occupied=False).values_list('number', flat=True)
            result[f'Floor {floor.number}'] = list(free_slots)
        return Response(result, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def occupied_slots(self, request):
        vehicle_type = request.query_params.get('vehicle_type')
        floors = Floor.objects.all()
        result = {}
        for floor in floors:
            occupied_slots = Slot.objects.filter(floor=floor, vehicle_type=vehicle_type, is_occupied=True).values_list('number', flat=True)
            result[f'Floor {floor.number}'] = list(occupied_slots)
        return Response(result, status=status.HTTP_200_OK)
