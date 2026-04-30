# inventory/views.py
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Item, StockTransaction
from .forms import ItemForm, StockTransactionForm


# Item Views
class ItemListView(ListView):
    model = Item
    template_name = 'inventory/item_list.html'
    context_object_name = 'items'
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


class ItemDetailView(DetailView):
    model = Item
    template_name = 'inventory/item_detail.html'
    context_object_name = 'item'


class ItemCreateView(SuccessMessageMixin, CreateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item_list')
    success_message = 'Item "%(name)s" was created successfully.'


class ItemUpdateView(SuccessMessageMixin, UpdateView):
    model = Item
    form_class = ItemForm
    template_name = 'inventory/item_form.html'
    success_url = reverse_lazy('item_list')
    success_message = 'Item "%(name)s" was updated successfully.'


class ItemDeleteView(SuccessMessageMixin, DeleteView):
    model = Item
    template_name = 'inventory/item_confirm_delete.html'
    success_url = reverse_lazy('item_list')
    success_message = 'Item was deleted successfully.'
    context_object_name = 'item'


# StockTransaction Views
class StockTransactionListView(ListView):
    model = StockTransaction
    template_name = 'inventory/stocktransaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20
    ordering = ['-date', '-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.GET.get('company')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        item_id = self.request.GET.get('item')
        if item_id:
            queryset = queryset.filter(item_id=item_id)
        type_filter = self.request.GET.get('type')
        if type_filter:
            queryset = queryset.filter(type=type_filter)
        return queryset


class StockTransactionDetailView(DetailView):
    model = StockTransaction
    template_name = 'inventory/stocktransaction_detail.html'
    context_object_name = 'transaction'


class StockTransactionCreateView(SuccessMessageMixin, CreateView):
    model = StockTransaction
    form_class = StockTransactionForm
    template_name = 'inventory/stocktransaction_form.html'
    success_url = reverse_lazy('stocktransaction_list')
    success_message = 'Stock transaction was created successfully.'


class StockTransactionUpdateView(SuccessMessageMixin, UpdateView):
    model = StockTransaction
    form_class = StockTransactionForm
    template_name = 'inventory/stocktransaction_form.html'
    success_url = reverse_lazy('stocktransaction_list')
    success_message = 'Stock transaction was updated successfully.'


class StockTransactionDeleteView(SuccessMessageMixin, DeleteView):
    model = StockTransaction
    template_name = 'inventory/stocktransaction_confirm_delete.html'
    success_url = reverse_lazy('stocktransaction_list')
    success_message = 'Stock transaction was deleted successfully.'
    context_object_name = 'transaction'
