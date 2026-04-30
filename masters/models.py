# masters/models.py
from django.db import models
from core.models import TimeStampedModel

class MasterType(TimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Master(TimeStampedModel):
    type = models.ForeignKey(MasterType, on_delete=models.CASCADE, related_name='masters')
    code = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ['type', 'code']

    def __str__(self):
        return f"{self.type.name} - {self.name}"