from rest_framework import viewsets, permissions
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import AuditLog
from .serializers import AuditLogSerializer


class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    """Read-only audit log viewer."""
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AuditLogSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['user', 'company', 'action', 'model_name', 'timestamp']
    search_fields = ['model_name', 'object_id', 'reason', 'new_value', 'old_value']
    ordering_fields = ['timestamp']
    ordering = ['-timestamp']

    def get_queryset(self):
        company_id = self.request.session.get('company_id')
        qs = AuditLog.objects.select_related('user', 'company')
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs

    @staticmethod
    def get_view_name():
        return "Audit Logs"
