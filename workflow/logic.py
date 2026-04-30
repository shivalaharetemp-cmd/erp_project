# workflow/logic.py
from django.utils import timezone
from .models import VehiclePlacement, Loading, Dispatch, Billing, WorkflowLog

def update_workflow_stage(instance, stage):
    WorkflowLog.objects.create(
        company=instance.company if hasattr(instance, 'company') else instance.placement.company,
        reference_id=str(instance.pk),
        stage=stage
    )

def create_vehicle_placement(company, vehicle, placement_time=None):
    vp = VehiclePlacement.objects.create(
        company=company,
        vehicle=vehicle,
        placement_time=placement_time or timezone.now(),
        status='VEHICLE_PLACED'
    )
    update_workflow_stage(vp, 'VEHICLE_PLACED')
    return vp

def start_loading(placement, supervisor):
    loading = Loading.objects.create(
        placement=placement,
        start_time=timezone.now(),
        supervisor=supervisor,
        status='LOADING_STARTED'
    )
    update_workflow_stage(loading, 'LOADING_STARTED')
    return loading

def complete_loading(loading):
    loading.end_time = timezone.now()
    loading.status = 'LOADING_COMPLETED'
    loading.save()
    update_workflow_stage(loading, 'LOADING_COMPLETED')
    return loading

def dispatch_vehicle(loading, destination, transporter):
    dispatch = Dispatch.objects.create(
        loading=loading,
        dispatch_time=timezone.now(),
        destination=destination,
        transporter=transporter,
        status='DISPATCHED'
    )
    update_workflow_stage(dispatch, 'DISPATCHED')
    return dispatch

def update_transit_status(dispatch, status):
    dispatch.status = status
    dispatch.save()
    update_workflow_stage(dispatch, status)

def create_billing(dispatch, invoice_number, amount):
    billing = Billing.objects.create(
        dispatch=dispatch,
        invoice_number=invoice_number,
        invoice_date=timezone.now().date(),
        amount=amount,
        status='BILLING_PENDING'
    )
    update_workflow_stage(billing, 'BILLING_PENDING')
    return billing

def mark_billed(billing):
    billing.status = 'BILLED'
    billing.save()
    update_workflow_stage(billing, 'BILLED')
    return billing