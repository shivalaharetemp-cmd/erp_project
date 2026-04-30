# workflow/views.py
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import VehiclePlacement, Loading, Dispatch, Billing, WorkflowLog
from .forms import VehiclePlacementForm, LoadingForm, DispatchForm, BillingForm, WorkflowLogForm


# VehiclePlacement Views
class VehiclePlacementListView(ListView):
    model = VehiclePlacement
    template_name = 'workflow/vehicleplacement_list.html'
    context_object_name = 'placements'
    paginate_by = 20
    ordering = ['-placement_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.GET.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class VehiclePlacementDetailView(DetailView):
    model = VehiclePlacement
    template_name = 'workflow/vehicleplacement_detail.html'
    context_object_name = 'placement'


class VehiclePlacementCreateView(SuccessMessageMixin, CreateView):
    model = VehiclePlacement
    form_class = VehiclePlacementForm
    template_name = 'workflow/vehicleplacement_form.html'
    success_url = reverse_lazy('vehicleplacement_list')
    success_message = 'Vehicle placement was created successfully.'


class VehiclePlacementUpdateView(SuccessMessageMixin, UpdateView):
    model = VehiclePlacement
    form_class = VehiclePlacementForm
    template_name = 'workflow/vehicleplacement_form.html'
    success_url = reverse_lazy('vehicleplacement_list')
    success_message = 'Vehicle placement was updated successfully.'


class VehiclePlacementDeleteView(SuccessMessageMixin, DeleteView):
    model = VehiclePlacement
    template_name = 'workflow/vehicleplacement_confirm_delete.html'
    success_url = reverse_lazy('vehicleplacement_list')
    success_message = 'Vehicle placement was deleted successfully.'
    context_object_name = 'placement'


# Loading Views
class LoadingListView(ListView):
    model = Loading
    template_name = 'workflow/loading_list.html'
    context_object_name = 'loadings'
    paginate_by = 20
    ordering = ['-start_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class LoadingDetailView(DetailView):
    model = Loading
    template_name = 'workflow/loading_detail.html'
    context_object_name = 'loading'


class LoadingCreateView(SuccessMessageMixin, CreateView):
    model = Loading
    form_class = LoadingForm
    template_name = 'workflow/loading_form.html'
    success_url = reverse_lazy('loading_list')
    success_message = 'Loading record was created successfully.'


class LoadingUpdateView(SuccessMessageMixin, UpdateView):
    model = Loading
    form_class = LoadingForm
    template_name = 'workflow/loading_form.html'
    success_url = reverse_lazy('loading_list')
    success_message = 'Loading record was updated successfully.'


class LoadingDeleteView(SuccessMessageMixin, DeleteView):
    model = Loading
    template_name = 'workflow/loading_confirm_delete.html'
    success_url = reverse_lazy('loading_list')
    success_message = 'Loading record was deleted successfully.'
    context_object_name = 'loading'


# Dispatch Views
class DispatchListView(ListView):
    model = Dispatch
    template_name = 'workflow/dispatch_list.html'
    context_object_name = 'dispatches'
    paginate_by = 20
    ordering = ['-dispatch_time']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class DispatchDetailView(DetailView):
    model = Dispatch
    template_name = 'workflow/dispatch_detail.html'
    context_object_name = 'dispatch'


class DispatchCreateView(SuccessMessageMixin, CreateView):
    model = Dispatch
    form_class = DispatchForm
    template_name = 'workflow/dispatch_form.html'
    success_url = reverse_lazy('dispatch_list')
    success_message = 'Dispatch was created successfully.'


class DispatchUpdateView(SuccessMessageMixin, UpdateView):
    model = Dispatch
    form_class = DispatchForm
    template_name = 'workflow/dispatch_form.html'
    success_url = reverse_lazy('dispatch_list')
    success_message = 'Dispatch was updated successfully.'


class DispatchDeleteView(SuccessMessageMixin, DeleteView):
    model = Dispatch
    template_name = 'workflow/dispatch_confirm_delete.html'
    success_url = reverse_lazy('dispatch_list')
    success_message = 'Dispatch was deleted successfully.'
    context_object_name = 'dispatch'


# Billing Views
class BillingListView(ListView):
    model = Billing
    template_name = 'workflow/billing_list.html'
    context_object_name = 'billings'
    paginate_by = 20
    ordering = ['-invoice_date']

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class BillingDetailView(DetailView):
    model = Billing
    template_name = 'workflow/billing_detail.html'
    context_object_name = 'billing'


class BillingCreateView(SuccessMessageMixin, CreateView):
    model = Billing
    form_class = BillingForm
    template_name = 'workflow/billing_form.html'
    success_url = reverse_lazy('billing_list')
    success_message = 'Billing record was created successfully.'


class BillingUpdateView(SuccessMessageMixin, UpdateView):
    model = Billing
    form_class = BillingForm
    template_name = 'workflow/billing_form.html'
    success_url = reverse_lazy('billing_list')
    success_message = 'Billing record was updated successfully.'


class BillingDeleteView(SuccessMessageMixin, DeleteView):
    model = Billing
    template_name = 'workflow/billing_confirm_delete.html'
    success_url = reverse_lazy('billing_list')
    success_message = 'Billing record was deleted successfully.'
    context_object_name = 'billing'
