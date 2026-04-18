from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Freight, ReturnFreight
from .serializers import FreightSerializer, ReturnFreightSerializer
from core.exceptions import ERPBusinessError


class FreightViewSet(viewsets.ModelViewSet):
    """Freight management for vehicles."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['vehicle', 'freight_type', 'is_active']
    ordering = ['-created_at']

    def get_queryset(self):
        company_id = self.request.session.get('company_id')
        qs = Freight.objects.select_related('vehicle', 'created_by')
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs

    def get_serializer_class(self):
        if self.action == 'return_freights':
            return ReturnFreightSerializer
        return FreightSerializer

    def perform_create(self, serializer):
        company_id = self.request.session.get('company_id')
        vehicle = serializer.validated_data['vehicle']

        # Validate vehicle status
        if vehicle.status in ('Delivered', 'Cancelled'):
            raise ERPBusinessError(
                f"Cannot add freight to vehicle with status: {vehicle.status}",
                code='FRE_001',
            )

        serializer.save(
            company_id=company_id,
            created_by=self.request.user,
        )

    @action(detail=False, methods=['get'], url_path='vehicle/(?P<vehicle_id>[^/.]+)')
    def by_vehicle(self, request, vehicle_id=None):
        """Get all freight for a specific vehicle."""
        company_id = request.session.get('company_id')
        qs = Freight.objects.filter(vehicle_id=vehicle_id)
        if company_id:
            qs = qs.filter(company_id=company_id)
        serializer = FreightSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='deactivate')
    def deactivate(self, request, pk=None):
        """Deactivate (reverse) a freight entry."""
        freight = self.get_object()
        if not freight.is_active:
            raise ERPBusinessError("Freight is already inactive.", code='FRE_001')
        freight.is_active = False
        freight.save()
        return Response({'detail': 'Freight deactivated.'})

    def perform_destroy(self, instance):
        """Prevent deletion - only deactivation."""
        raise ERPBusinessError(
            "Freights cannot be deleted. Use the deactivate endpoint instead.",
            code='FRE_001',
        )
