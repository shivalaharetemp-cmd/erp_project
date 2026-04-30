# accounts/views.py
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import MasterGroup, Ledger, Voucher, VoucherEntry
from .forms import MasterGroupForm, LedgerForm, VoucherForm, VoucherEntryFormSet


# MasterGroup Views
class MasterGroupListView(ListView):
    model = MasterGroup
    template_name = 'accounts/mastergroup_list.html'
    context_object_name = 'groups'
    paginate_by = 20
    ordering = ['type', 'name']


class MasterGroupDetailView(DetailView):
    model = MasterGroup
    template_name = 'accounts/mastergroup_detail.html'
    context_object_name = 'group'


class MasterGroupCreateView(SuccessMessageMixin, CreateView):
    model = MasterGroup
    form_class = MasterGroupForm
    template_name = 'accounts/mastergroup_form.html'
    success_url = reverse_lazy('mastergroup_list')
    success_message = 'Group "%(name)s" was created successfully.'


class MasterGroupUpdateView(SuccessMessageMixin, UpdateView):
    model = MasterGroup
    form_class = MasterGroupForm
    template_name = 'accounts/mastergroup_form.html'
    success_url = reverse_lazy('mastergroup_list')
    success_message = 'Group "%(name)s" was updated successfully.'


class MasterGroupDeleteView(SuccessMessageMixin, DeleteView):
    model = MasterGroup
    template_name = 'accounts/mastergroup_confirm_delete.html'
    success_url = reverse_lazy('mastergroup_list')
    success_message = 'Group was deleted successfully.'
    context_object_name = 'group'


# Ledger Views
class LedgerListView(ListView):
    model = Ledger
    template_name = 'accounts/ledger_list.html'
    context_object_name = 'ledgers'
    paginate_by = 20
    ordering = ['company__name', 'name']

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.GET.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(name__icontains=search)
        return queryset


class LedgerDetailView(DetailView):
    model = Ledger
    template_name = 'accounts/ledger_detail.html'
    context_object_name = 'ledger'


class LedgerCreateView(SuccessMessageMixin, CreateView):
    model = Ledger
    form_class = LedgerForm
    template_name = 'accounts/ledger_form.html'
    success_url = reverse_lazy('ledger_list')
    success_message = 'Ledger "%(name)s" was created successfully.'


class LedgerUpdateView(SuccessMessageMixin, UpdateView):
    model = Ledger
    form_class = LedgerForm
    template_name = 'accounts/ledger_form.html'
    success_url = reverse_lazy('ledger_list')
    success_message = 'Ledger "%(name)s" was updated successfully.'


class LedgerDeleteView(SuccessMessageMixin, DeleteView):
    model = Ledger
    template_name = 'accounts/ledger_confirm_delete.html'
    success_url = reverse_lazy('ledger_list')
    success_message = 'Ledger was deleted successfully.'
    context_object_name = 'ledger'


# Voucher Views
class VoucherListView(ListView):
    model = Voucher
    template_name = 'accounts/voucher_list.html'
    context_object_name = 'vouchers'
    paginate_by = 20
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.GET.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        return queryset


class VoucherDetailView(DetailView):
    model = Voucher
    template_name = 'accounts/voucher_detail.html'
    context_object_name = 'voucher'


class VoucherCreateView(SuccessMessageMixin, CreateView):
    model = Voucher
    form_class = VoucherForm
    template_name = 'accounts/voucher_form.html'
    success_url = reverse_lazy('voucher_list')
    success_message = 'Voucher was created successfully.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = VoucherEntryFormSet(self.request.POST)
        else:
            context['formset'] = VoucherEntryFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class VoucherUpdateView(SuccessMessageMixin, UpdateView):
    model = Voucher
    form_class = VoucherForm
    template_name = 'accounts/voucher_form.html'
    success_url = reverse_lazy('voucher_list')
    success_message = 'Voucher was updated successfully.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = VoucherEntryFormSet(self.request.POST, instance=self.object)
        else:
            context['formset'] = VoucherEntryFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        if formset.is_valid():
            self.object = form.save()
            formset.instance = self.object
            formset.save()
            return super().form_valid(form)
        else:
            return self.render_to_response(self.get_context_data(form=form))


class VoucherDeleteView(SuccessMessageMixin, DeleteView):
    model = Voucher
    template_name = 'accounts/voucher_confirm_delete.html'
    success_url = reverse_lazy('voucher_list')
    success_message = 'Voucher was deleted successfully.'
    context_object_name = 'voucher'
