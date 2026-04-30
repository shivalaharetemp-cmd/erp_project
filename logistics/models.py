# logistics/models.py
from django.db import models
from django.core.validators import RegexValidator
from core.models import TimeStampedModel
from company.models import Company
from masters.models import Master

class Vehicle(TimeStampedModel):
    vehicle_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(r'^[A-Z]{2}\d{2}[A-Z]{1,2}\d{4}$', 'Invalid vehicle number')]
    )
    vehicle_type = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        limit_choices_to={'type__code': 'VEHICLE_TYPE'}
    )

    def __str__(self):
        return self.vehicle_number

class Shipment(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    supply_type = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        related_name='supply_type_shipments',
        limit_choices_to={'type__code': 'SUPPLY_TYPE'}
    )
    sub_supply_type = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        related_name='sub_supply_type_shipments',
        limit_choices_to={'type__code': 'SUB_SUPPLY_TYPE'}
    )
    document_type = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        related_name='document_type_shipments',
        limit_choices_to={'type__code': 'DOCUMENT_TYPE'}
    )
    transportation_mode = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        related_name='transportation_mode_shipments',
        limit_choices_to={'type__code': 'TRANSPORTATION_MODE'}
    )
    consignment_status = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        related_name='consignment_status_shipments',
        limit_choices_to={'type__code': 'CONSIGNMENT_STATUS'}
    )
    vehicle = models.ForeignKey(Vehicle, on_delete=models.PROTECT)
    transaction_type = models.ForeignKey(
        Master,
        on_delete=models.PROTECT,
        related_name='transaction_type_shipments',
        limit_choices_to={'type__code': 'TRANSACTION_TYPE'}
    )
    date = models.DateField()

    def __str__(self):
        return f"{self.company.name} - {self.vehicle.vehicle_number}"