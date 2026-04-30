# company/views.py
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Company
from .forms import CompanyForm


class CompanyListView(ListView):
    model = Company
    template_name = 'company/company_list.html'
    context_object_name = 'companies'
    paginate_by = 20
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class CompanyDetailView(DetailView):
    model = Company
    template_name = 'company/company_detail.html'
    context_object_name = 'company'


class CompanyCreateView(SuccessMessageMixin, CreateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('company_list')
    success_message = 'Company "%(name)s" was created successfully.'


class CompanyUpdateView(SuccessMessageMixin, UpdateView):
    model = Company
    form_class = CompanyForm
    template_name = 'company/company_form.html'
    success_url = reverse_lazy('company_list')
    success_message = 'Company "%(name)s" was updated successfully.'


class CompanyDeleteView(SuccessMessageMixin, DeleteView):
    model = Company
    template_name = 'company/company_confirm_delete.html'
    success_url = reverse_lazy('company_list')
    success_message = 'Company was deleted successfully.'
    context_object_name = 'company'
