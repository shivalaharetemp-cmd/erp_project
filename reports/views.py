# reports/views.py
from django.shortcuts import render
from django.db.models import Sum, Q, Count, Avg, F
from django.utils.dateparse import parse_date
from company.models import Company
from accounts.models import VoucherEntry, Ledger, Voucher, MasterGroup
from inventory.models import StockTransaction, Item
from logistics.models import Vehicle, Shipment
from workflow.models import WorkflowLog, VehiclePlacement, Loading, Dispatch, Billing
from .forms import (
    LedgerFilterForm, StockFilterForm, VoucherFilterForm,
    VehicleFilterForm, DateRangeForm, CompanyFilterForm
)

# ─── LEDGER REPORT ──────────────────────────────────────────────────────────
def ledger_report(request):
    form = LedgerFilterForm(request.GET or None)
    company_id = request.GET.get('company')
    ledger_id = request.GET.get('ledger')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    ledgers = Ledger.objects.all()
    if company_id:
        ledgers = ledgers.filter(company_id=company_id)
    if ledger_id:
        ledgers = ledgers.filter(id=ledger_id)

    report_data = []
    total_debit_all = 0
    total_credit_all = 0
    total_closing_all = 0

    for ledger in ledgers:
        entries = VoucherEntry.objects.filter(ledger=ledger)
        if company_id:
            entries = entries.filter(voucher__company_id=company_id)
        if start_date:
            entries = entries.filter(voucher__date__gte=start_date)
        if end_date:
            entries = entries.filter(voucher__date__lte=end_date)

        total_debit = entries.aggregate(Sum('debit'))['debit__sum'] or 0
        total_credit = entries.aggregate(Sum('credit'))['credit__sum'] or 0
        opening = 0
        closing = opening + total_debit - total_credit
        total_debit_all += total_debit
        total_credit_all += total_credit
        total_closing_all += closing

        report_data.append({
            'ledger': ledger,
            'opening': opening,
            'debit': total_debit,
            'credit': total_credit,
            'closing': closing,
            'entries_count': entries.count(),
        })

    return render(request, 'reports/ledger_report.html', {
        'report_data': report_data,
        'form': form,
        'total_debit': total_debit_all,
        'total_credit': total_credit_all,
        'total_closing': total_closing_all,
    })


# ─── STOCK / INVENTORY REPORT ───────────────────────────────────────────────
def stock_report(request):
    form = StockFilterForm(request.GET or None)
    company_id = request.GET.get('company')
    item_id = request.GET.get('item')

    items_qs = Item.objects.all()
    if company_id:
        items_qs = items_qs.filter(company_id=company_id)
    if item_id:
        items_qs = items_qs.filter(id=item_id)

    report_data = []
    total_inward = 0
    total_outward = 0
    total_balance = 0

    for item in items_qs.prefetch_related('stocktransaction_set'):
        txns = item.stocktransaction_set.all()
        if company_id:
            txns = txns.filter(company_id=company_id)

        inward = txns.filter(type='IN').aggregate(Sum('quantity'))['quantity__sum'] or 0
        outward = txns.filter(type='OUT').aggregate(Sum('quantity'))['quantity__sum'] or 0
        opening = 0
        balance = opening + inward - outward
        total_inward += inward
        total_outward += outward
        total_balance += balance

        report_data.append({
            'item': item,
            'company': item.company,
            'opening': opening,
            'inward': inward,
            'outward': outward,
            'balance': balance,
            'txns_count': txns.count(),
        })

    return render(request, 'reports/stock_report.html', {
        'report_data': report_data,
        'form': form,
        'total_inward': total_inward,
        'total_outward': total_outward,
        'total_balance': total_balance,
    })


# ─── WORKFLOW / OPERATIONS REPORT ─────────────────────────────────────────
def workflow_report(request):
    form = CompanyFilterForm(request.GET or None)
    company_id = request.GET.get('company')
    company_filter = {}
    if company_id:
        company_filter = {'company_id': company_id}

    vehicles = VehiclePlacement.objects.filter(**company_filter)
    report_data = []

    total_waiting = 0
    total_loading = 0
    count_waiting = 0
    count_loading = 0
    status_counts = {}
    billing_status_counts = {}

    for vp in vehicles.select_related('vehicle', 'company').prefetch_related('vehicle__shipment_set'):
        loading = Loading.objects.filter(placement=vp).first()
        dispatch = Dispatch.objects.filter(loading=loading).first() if loading else None
        billing = Billing.objects.filter(dispatch=dispatch).first() if dispatch else None

        waiting_time = None
        if vp.placement_time and loading and loading.start_time:
            waiting_time = round((loading.start_time - vp.placement_time).total_seconds() / 3600, 2)
            total_waiting += waiting_time
            count_waiting += 1

        loading_time = None
        if loading and loading.start_time and loading.end_time:
            loading_time = round((loading.end_time - loading.start_time).total_seconds() / 3600, 2)
            total_loading += loading_time
            count_loading += 1

        status = dispatch.status if dispatch else 'N/A'
        billing_status = billing.status if billing else 'N/A'
        status_counts[status] = status_counts.get(status, 0) + 1
        billing_status_counts[billing_status] = billing_status_counts.get(billing_status, 0) + 1

        report_data.append({
            'vehicle': vp.vehicle.vehicle_number,
            'company': vp.company.name,
            'waiting_time': waiting_time,
            'loading_time': loading_time,
            'status': status,
            'billing_status': billing_status,
            'placement_time': vp.placement_time,
        })

    avg_waiting = round(total_waiting / count_waiting, 2) if count_waiting else 0
    avg_loading = round(total_loading / count_loading, 2) if count_loading else 0

    return render(request, 'reports/workflow_report.html', {
        'report_data': report_data,
        'form': form,
        'status_counts': status_counts,
        'billing_status_counts': billing_status_counts,
        'avg_waiting': avg_waiting,
        'avg_loading': avg_loading,
    })


# ─── VOUCHER / SALES & PURCHASE REPORT ──────────────────────────────────────
def voucher_report(request):
    form = VoucherFilterForm(request.GET or None)
    company_id = request.GET.get('company')
    voucher_type = request.GET.get('voucher_type')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    vouchers = Voucher.objects.all().select_related('company').prefetch_related('entries')
    if company_id:
        vouchers = vouchers.filter(company_id=company_id)
    if voucher_type:
        vouchers = vouchers.filter(type=voucher_type)
    if start_date:
        vouchers = vouchers.filter(date__gte=start_date)
    if end_date:
        vouchers = vouchers.filter(date__lte=end_date)

    total_debit = 0
    total_credit = 0
    type_counts = {}
    company_totals = {}

    for v in vouchers:
        vd = v.entries.aggregate(d=Sum('debit'), c=Sum('credit'))
        v.total_debit = vd['d'] or 0
        v.total_credit = vd['c'] or 0
        total_debit += v.total_debit
        total_credit += v.total_credit
        type_counts[v.type] = type_counts.get(v.type, 0) + 1
        company_totals[v.company.name] = company_totals.get(v.company.name, {'debit': 0, 'credit': 0, 'count': 0})
        company_totals[v.company.name]['debit'] += v.total_debit
        company_totals[v.company.name]['credit'] += v.total_credit
        company_totals[v.company.name]['count'] += 1

    return render(request, 'reports/voucher_report.html', {
        'vouchers': vouchers,
        'form': form,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'type_counts': type_counts,
        'company_totals': company_totals,
    })


# ─── FINANCIAL SUMMARY REPORT ──────────────────────────────────────────────
def financial_summary(request):
    form = DateRangeForm(request.GET or None)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    entries = VoucherEntry.objects.all()
    txns = StockTransaction.objects.all()
    billings = Billing.objects.all()

    if start_date:
        entries = entries.filter(voucher__date__gte=start_date)
        txns = txns.filter(date__gte=start_date)
        billings = billings.filter(invoice_date__gte=start_date)
    if end_date:
        entries = entries.filter(voucher__date__lte=end_date)
        txns = txns.filter(date__lte=end_date)
        billings = billings.filter(invoice_date__lte=end_date)

    total_debit = entries.aggregate(Sum('debit'))['debit__sum'] or 0
    total_credit = entries.aggregate(Sum('credit'))['credit__sum'] or 0
    stock_in = txns.filter(type='IN').aggregate(Sum('quantity'))['quantity__sum'] or 0
    stock_out = txns.filter(type='OUT').aggregate(Sum('quantity'))['quantity__sum'] or 0
    total_billing = billings.aggregate(Sum('amount'))['amount__sum'] or 0
    pending_billing = billings.filter(status='BILLING_PENDING').aggregate(Sum('amount'))['amount__sum'] or 0

    # Group-wise ledger totals
    group_totals = {}
    for g in MasterGroup.objects.all():
        g_debit = entries.filter(ledger__group=g).aggregate(Sum('debit'))['debit__sum'] or 0
        g_credit = entries.filter(ledger__group=g).aggregate(Sum('credit'))['credit__sum'] or 0
        group_totals[g.name] = {'debit': g_debit, 'credit': g_credit, 'type': g.type}

    return render(request, 'reports/financial_summary.html', {
        'form': form,
        'total_debit': total_debit,
        'total_credit': total_credit,
        'stock_in': stock_in,
        'stock_out': stock_out,
        'total_billing': total_billing,
        'pending_billing': pending_billing,
        'group_totals': group_totals,
        'entries_count': entries.count(),
        'txns_count': txns.count(),
        'vouchers_count': Voucher.objects.filter().count(),
    })


# ─── VEHICLE UTILIZATION REPORT ────────────────────────────────────────────
def vehicle_report(request):
    form = VehicleFilterForm(request.GET or None)
    vehicle_id = request.GET.get('vehicle')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    vehicles = Vehicle.objects.all()
    if vehicle_id:
        vehicles = vehicles.filter(id=vehicle_id)

    report_data = []
    for v in vehicles:
        placements = VehiclePlacement.objects.filter(vehicle=v)
        shipments = Shipment.objects.filter(vehicle=v)
        if start_date:
            placements = placements.filter(placement_time__date__gte=start_date)
            shipments = shipments.filter(date__gte=start_date)
        if end_date:
            placements = placements.filter(placement_time__date__lte=end_date)
            shipments = shipments.filter(date__lte=end_date)

        report_data.append({
            'vehicle': v,
            'placements_count': placements.count(),
            'shipments_count': shipments.count(),
            'type': v.vehicle_type.name if v.vehicle_type else '-',
        })

    return render(request, 'reports/vehicle_report.html', {
        'report_data': report_data,
        'form': form,
    })


# ─── COMPANY-WIDE SUMMARY REPORT ─────────────────────────────────────────────
def company_summary(request):
    report_data = []
    for company in Company.objects.filter(is_active=True):
        ledgers = Ledger.objects.filter(company=company).count()
        ledger_entries = VoucherEntry.objects.filter(voucher__company=company)
        total_debit = ledger_entries.aggregate(Sum('debit'))['debit__sum'] or 0
        total_credit = ledger_entries.aggregate(Sum('credit'))['credit__sum'] or 0
        items = Item.objects.filter(company=company).count()
        stock_txns = StockTransaction.objects.filter(company=company).count()
        shipments = Shipment.objects.filter(company=company).count()
        placements = VehiclePlacement.objects.filter(company=company).count()
        vouchers = Voucher.objects.filter(company=company).count()

        report_data.append({
            'company': company,
            'ledgers': ledgers,
            'vouchers': vouchers,
            'total_debit': total_debit,
            'total_credit': total_credit,
            'items': items,
            'stock_txns': stock_txns,
            'shipments': shipments,
            'placements': placements,
        })

    return render(request, 'reports/company_summary.html', {
        'report_data': report_data,
    })