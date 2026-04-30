# core/views.py
from django.shortcuts import render
from django.db.models import Count, Sum
from company.models import Company
from accounts.models import Ledger, Voucher
from inventory.models import Item, StockTransaction
from logistics.models import Vehicle, Shipment
from workflow.models import VehiclePlacement, Loading, Dispatch, Billing


def dashboard(request):
    context = {
        'total_companies': Company.objects.filter(is_active=True).count(),
        'total_ledgers': Ledger.objects.count(),
        'total_items': Item.objects.count(),
        'total_vehicles': Vehicle.objects.count(),
        'active_shipments': Shipment.objects.count(),
        'pending_placements': VehiclePlacement.objects.filter(status='PLACED').count(),
        'active_loadings': Loading.objects.filter(status='LOADING').count(),
        'pending_billing': Billing.objects.filter(status='BILLING_PENDING').count(),
        'recent_vouchers': Voucher.objects.select_related('company').order_by('-created_at')[:5],
        'recent_transactions': StockTransaction.objects.select_related('item', 'company').order_by('-created_at')[:5],
    }
    return render(request, 'core/dashboard.html', context)
