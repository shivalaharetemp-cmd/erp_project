# inventory/models.py
from django.db import models
from core.models import TimeStampedModel
from company.models import Company

class Item(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)

    class Meta:
        unique_together = ['company', 'name']

    def __str__(self):
        return f"{self.company.name} - {self.name}"

class StockTransaction(TimeStampedModel):
    TRANSACTION_TYPES = [
        ('IN', 'Inward'),
        ('OUT', 'Outward'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=15, decimal_places=2)
    type = models.CharField(max_length=3, choices=TRANSACTION_TYPES)
    reference = models.CharField(max_length=200, blank=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.item.name} - {self.type} - {self.quantity}"