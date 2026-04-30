# logistics/views.py
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Vehicle, Shipment
from .forms import VehicleForm, ShipmentForm


# Vehicle Views
class VehicleListView(ListView):
    model = Vehicle
    template_name = 'logistics/vehicle_list.html'
    context_object_name = 'vehicles'
    paginate_by = 20
    ordering = ['vehicle_number']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(vehicle_number__icontains=search.upper())
        return queryset


class VehicleDetailView(DetailView):
    model = Vehicle
    template_name = 'logistics/vehicle_detail.html'
    context_object_name = 'vehicle'


class VehicleCreateView(SuccessMessageMixin, CreateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'logistics/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')
    success_message = 'Vehicle "%(vehicle_number)s" was created successfully.'


class VehicleUpdateView(SuccessMessageMixin, UpdateView):
    model = Vehicle
    form_class = VehicleForm
    template_name = 'logistics/vehicle_form.html'
    success_url = reverse_lazy('vehicle_list')
    success_message = 'Vehicle "%(vehicle_number)s" was updated successfully.'


class VehicleDeleteView(SuccessMessageMixin, DeleteView):
    model = Vehicle
    template_name = 'logistics/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicle_list')
    success_message = 'Vehicle was deleted successfully.'
    context_object_name = 'vehicle'


# Shipment Views
class ShipmentListView(ListView):
    model = Shipment
    template_name = 'logistics/shipment_list.html'
    context_object_name = 'shipments'
    paginate_by = 20
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.GET.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        vehicle_id = self.request.GET.get('vehicle')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        return queryset


class ShipmentDetailView(DetailView):
    model = Shipment
    template_name = 'logistics/shipment_detail.html'
    context_object_name = 'shipment'


class ShipmentCreateView(SuccessMessageMixin, CreateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'logistics/shipment_form.html'
    success_url = reverse_lazy('shipment_list')
    success_message = 'Shipment was created successfully.'


class ShipmentUpdateView(SuccessMessageMixin, UpdateView):
    model = Shipment
    form_class = ShipmentForm
    template_name = 'logistics/shipment_form.html'
    success_url = reverse_lazy('shipment_list')
    success_message = 'Shipment was updated successfully.'


class ShipmentDeleteView(SuccessMessageMixin, DeleteView):
    model = Shipment
    template_name = 'logistics/shipment_confirm_delete.html'
    success_url = reverse_lazy('shipment_list')
    success_message = 'Shipment was deleted successfully.'
    context_object_name = 'shipment'
