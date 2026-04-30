# core/admin.py
from django.contrib import admin

class CompanyAdminMixin:
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser:
            return qs
        return qs.filter(company__in=request.user.companies.all())