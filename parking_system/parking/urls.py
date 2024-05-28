from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParkingLotViewSet

router = DefaultRouter()
router.register(r'parking_lot', ParkingLotViewSet, basename='parking_lot')

urlpatterns = [
    path('', include(router.urls)),
    

]
