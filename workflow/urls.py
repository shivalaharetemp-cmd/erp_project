# workflow/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # VehiclePlacement URLs
    path('placements/', views.VehiclePlacementListView.as_view(), name='vehicleplacement_list'),
    path('placements/create/', views.VehiclePlacementCreateView.as_view(), name='vehicleplacement_create'),
    path('placements/<int:pk>/', views.VehiclePlacementDetailView.as_view(), name='vehicleplacement_detail'),
    path('placements/<int:pk>/update/', views.VehiclePlacementUpdateView.as_view(), name='vehicleplacement_update'),
    path('placements/<int:pk>/delete/', views.VehiclePlacementDeleteView.as_view(), name='vehicleplacement_delete'),
    
    # Loading URLs
    path('loadings/', views.LoadingListView.as_view(), name='loading_list'),
    path('loadings/create/', views.LoadingCreateView.as_view(), name='loading_create'),
    path('loadings/<int:pk>/', views.LoadingDetailView.as_view(), name='loading_detail'),
    path('loadings/<int:pk>/update/', views.LoadingUpdateView.as_view(), name='loading_update'),
    path('loadings/<int:pk>/delete/', views.LoadingDeleteView.as_view(), name='loading_delete'),
    
    # Dispatch URLs
    path('dispatches/', views.DispatchListView.as_view(), name='dispatch_list'),
    path('dispatches/create/', views.DispatchCreateView.as_view(), name='dispatch_create'),
    path('dispatches/<int:pk>/', views.DispatchDetailView.as_view(), name='dispatch_detail'),
    path('dispatches/<int:pk>/update/', views.DispatchUpdateView.as_view(), name='dispatch_update'),
    path('dispatches/<int:pk>/delete/', views.DispatchDeleteView.as_view(), name='dispatch_delete'),
    
    # Billing URLs
    path('billings/', views.BillingListView.as_view(), name='billing_list'),
    path('billings/create/', views.BillingCreateView.as_view(), name='billing_create'),
    path('billings/<int:pk>/', views.BillingDetailView.as_view(), name='billing_detail'),
    path('billings/<int:pk>/update/', views.BillingUpdateView.as_view(), name='billing_update'),
    path('billings/<int:pk>/delete/', views.BillingDeleteView.as_view(), name='billing_delete'),
]
