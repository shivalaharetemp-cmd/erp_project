# masters/views.py
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import MasterType, Master
from .forms import MasterTypeForm, MasterForm


# MasterType Views
class MasterTypeListView(ListView):
    model = MasterType
    template_name = 'masters/mastertype_list.html'
    context_object_name = 'mastertypes'
    paginate_by = 20
    ordering = ['name']


class MasterTypeDetailView(DetailView):
    model = MasterType
    template_name = 'masters/mastertype_detail.html'
    context_object_name = 'mastertype'


class MasterTypeCreateView(SuccessMessageMixin, CreateView):
    model = MasterType
    form_class = MasterTypeForm
    template_name = 'masters/mastertype_form.html'
    success_url = reverse_lazy('master_type_list')
    success_message = 'Master Type "%(name)s" was created successfully.'


class MasterTypeUpdateView(SuccessMessageMixin, UpdateView):
    model = MasterType
    form_class = MasterTypeForm
    template_name = 'masters/mastertype_form.html'
    success_url = reverse_lazy('master_type_list')
    success_message = 'Master Type "%(name)s" was updated successfully.'


class MasterTypeDeleteView(SuccessMessageMixin, DeleteView):
    model = MasterType
    template_name = 'masters/mastertype_confirm_delete.html'
    success_url = reverse_lazy('master_type_list')
    success_message = 'Master Type was deleted successfully.'
    context_object_name = 'mastertype'


# Master Views
class MasterListView(ListView):
    model = Master
    template_name = 'masters/master_list.html'
    context_object_name = 'masters'
    paginate_by = 20
    ordering = ['type__name', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        type_id = self.request.GET.get('type')
        if type_id:
            queryset = queryset.filter(type_id=type_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['master_types'] = MasterType.objects.all()
        return context


class MasterDetailView(DetailView):
    model = Master
    template_name = 'masters/master_detail.html'
    context_object_name = 'master'


class MasterCreateView(SuccessMessageMixin, CreateView):
    model = Master
    form_class = MasterForm
    template_name = 'masters/master_form.html'
    success_url = reverse_lazy('master_list')
    success_message = 'Master "%(name)s" was created successfully.'


class MasterUpdateView(SuccessMessageMixin, UpdateView):
    model = Master
    form_class = MasterForm
    template_name = 'masters/master_form.html'
    success_url = reverse_lazy('master_list')
    success_message = 'Master "%(name)s" was updated successfully.'


class MasterDeleteView(SuccessMessageMixin, DeleteView):
    model = Master
    template_name = 'masters/master_confirm_delete.html'
    success_url = reverse_lazy('master_list')
    success_message = 'Master was deleted successfully.'
    context_object_name = 'master'
