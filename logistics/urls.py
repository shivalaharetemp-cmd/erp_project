# logistics/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Vehicle URLs
    path('vehicles/', views.VehicleListView.as_view(), name='vehicle_list'),
    path('vehicles/create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('vehicles/<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('vehicles/<int:pk>/update/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
    
    # Shipment URLs
    path('shipments/', views.ShipmentListView.as_view(), name='shipment_list'),
    path('shipments/create/', views.ShipmentCreateView.as_view(), name='shipment_create'),
    path('shipments/<int:pk>/', views.ShipmentDetailView.as_view(), name='shipment_detail'),
    path('shipments/<int:pk>/update/', views.ShipmentUpdateView.as_view(), name='shipment_update'),
    path('shipments/<int:pk>/delete/', views.ShipmentDeleteView.as_view(), name='shipment_delete'),
]
