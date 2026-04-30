# workflow/models.py
from django.db import models
from core.models import TimeStampedModel
from company.models import Company
from logistics.models import Vehicle

class VehiclePlacement(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    placement_time = models.DateTimeField()
    status = models.CharField(max_length=50, default='PLACED')

    def __str__(self):
        return f"{self.company.name} - {self.vehicle.vehicle_number}"

class Loading(TimeStampedModel):
    placement = models.ForeignKey(VehiclePlacement, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    supervisor = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default='LOADING')

    def __str__(self):
        return f"Loading - {self.placement.vehicle.vehicle_number}"

class Dispatch(TimeStampedModel):
    loading = models.ForeignKey(Loading, on_delete=models.CASCADE)
    dispatch_time = models.DateTimeField()
    destination = models.CharField(max_length=300)
    transporter = models.CharField(max_length=200)
    status = models.CharField(max_length=50, default='DISPATCHED')

    def __str__(self):
        return f"Dispatch - {self.loading.placement.vehicle.vehicle_number}"

class Billing(TimeStampedModel):
    dispatch = models.ForeignKey(Dispatch, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=100)
    invoice_date = models.DateField()
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    status = models.CharField(max_length=50, default='BILLING_PENDING')

    def __str__(self):
        return f"Billing - {self.invoice_number}"

class WorkflowLog(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    reference_id = models.CharField(max_length=100)
    stage = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.company.name} - {self.stage} - {self.reference_id}"