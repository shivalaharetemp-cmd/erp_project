from rest_framework import viewsets, permissions, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Party, Item, Transporter, PurchaseOrder, PurchaseOrderItem
from .serializers import (
    PartySerializer, ItemSerializer, TransporterSerializer,
    PurchaseOrderSerializer, PurchaseOrderItemSerializer,
)


class CompanyFilterMixin:
    """Mixin to filter queryset by company from request session."""

    def get_queryset(self):
        queryset = super().get_queryset()
        company_id = self.request.session.get('company_id')
        if company_id:
            queryset = queryset.filter(company_id=company_id)
        return queryset

    def perform_create(self, serializer):
        company_id = self.request.session.get('company_id')
        serializer.save(company_id=company_id)


class PartyViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Party.objects.filter(is_active=True)
    serializer_class = PartySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['party_type', 'state_code']
    search_fields = ['party_name', 'party_code', 'gstin']
    ordering_fields = ['party_name', 'created_at']
    ordering = ['party_name']

    def perform_destroy(self, instance):
        """Soft delete - don't actually delete."""
        instance.is_active = False
        instance.save()


class ItemViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Item.objects.filter(is_active=True)
    serializer_class = ItemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['unit', 'tax_type']
    search_fields = ['item_name', 'item_code', 'hsn_code']
    ordering_fields = ['item_name', 'created_at']
    ordering = ['item_name']

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class TransporterViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = Transporter.objects.filter(is_active=True)
    serializer_class = TransporterSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'gstin', 'phone']
    ordering_fields = ['name', 'created_at']
    ordering = ['name']

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()


class PurchaseOrderViewSet(CompanyFilterMixin, viewsets.ModelViewSet):
    queryset = PurchaseOrder.objects.all()
    serializer_class = PurchaseOrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['party', 'status']
    search_fields = ['po_number']
    ordering_fields = ['po_date', 'created_at']
    ordering = ['-po_date']

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        po = self.get_object()
        items = po.items.all()
        serializer = PurchaseOrderItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        po = self.get_object()
        if po.status == 'Draft':
            po.status = 'Confirmed'
            po.save()
        return Response({'status': po.status})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        po = self.get_object()
        if po.status in ('Draft', 'Confirmed'):
            po.status = 'Cancelled'
            po.save()
        return Response({'status': po.status})
