# accounts/models.py
from django.db import models
from django.core.exceptions import ValidationError
from core.models import TimeStampedModel
from company.models import Company

class MasterGroup(TimeStampedModel):
    GROUP_TYPES = [
        ('ASSET', 'Asset'),
        ('LIABILITY', 'Liability'),
        ('INCOME', 'Income'),
        ('EXPENSE', 'Expense'),
    ]
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    type = models.CharField(max_length=20, choices=GROUP_TYPES)

    def __str__(self):
        return self.name

class Ledger(TimeStampedModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    group = models.ForeignKey(MasterGroup, on_delete=models.PROTECT)

    class Meta:
        unique_together = ['company', 'name']

    def __str__(self):
        return f"{self.company.name} - {self.name}"

class Voucher(TimeStampedModel):
    VOUCHER_TYPES = [
        ('PAYMENT', 'Payment'),
        ('RECEIPT', 'Receipt'),
        ('CONTRA', 'Contra'),
        ('JOURNAL', 'Journal'),
        ('SALES', 'Sales'),
        ('PURCHASE', 'Purchase'),
    ]
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    date = models.DateField()
    type = models.CharField(max_length=20, choices=VOUCHER_TYPES)
    reference = models.CharField(max_length=200, blank=True)

    def clean(self):
        if self.pk:
            entries = self.entries.all()
            if entries:
                total_debit = sum(e.debit for e in entries)
                total_credit = sum(e.credit for e in entries)
                if total_debit != total_credit:
                    raise ValidationError("Debit and Credit must be equal")

    def __str__(self):
        return f"{self.company.name} - {self.type} - {self.reference}"

class VoucherEntry(models.Model):
    voucher = models.ForeignKey(Voucher, on_delete=models.CASCADE, related_name='entries')
    ledger = models.ForeignKey(Ledger, on_delete=models.PROTECT)
    debit = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    credit = models.DecimalField(max_digits=15, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.ledger.name} - D:{self.debit} C:{self.credit}"