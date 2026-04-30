# company/models.py
from django.db import models
from core.models import TimeStampedModel

class Company(TimeStampedModel):
    name = models.CharField(max_length=200)
    gst_number = models.CharField(max_length=15, unique=True)
    address = models.TextField()
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name