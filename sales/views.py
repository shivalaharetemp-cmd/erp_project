from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Sale, SaleItem, CreditNote, CreditNoteItem
from .serializers import (
    SaleListSerializer, SaleDetailSerializer, CreateSaleSerializer,
    CreditNoteListSerializer, CreditNoteDetailSerializer, CreditNoteCreateSerializer,
)
from .services import SaleService
from core.exceptions import ERPBusinessError


class SaleViewSet(viewsets.ModelViewSet):
    """Sales invoice management."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['party', 'status', 'financial_year', 'invoice_date']
    search_fields = ['invoice_number', 'party__party_name', 'vehicle__vehicle_number']
    ordering_fields = ['invoice_date', 'created_at', 'grand_total']
    ordering = ['-invoice_date']

    def get_queryset(self):
        company_id = self.request.session.get('company_id')
        qs = Sale.objects.select_related('party', 'vehicle', 'created_by').prefetch_related('items')
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return SaleListSerializer
        elif self.action == 'retrieve':
            return SaleDetailSerializer
        elif self.action == 'create':
            return CreateSaleSerializer
        return SaleListSerializer

    def create(self, request, *args, **kwargs):
        """Create sale/invoice from vehicle."""
        serializer = CreateSaleSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vehicle_id = request.data.get('vehicle_id')
        if not vehicle_id:
            return Response({'error': 'vehicle_id is required.'}, status=400)

        from vehicles.models import Vehicle
        try:
            vehicle = Vehicle.objects.get(id=vehicle_id)
        except Vehicle.DoesNotExist:
            return Response({'error': 'Vehicle not found.'}, status=404)

        if vehicle.status != 'Loaded':
            return Response(
                {'error': f'Vehicle must be Loaded to create sale. Current: {vehicle.status}'},
                status=400,
            )

        try:
            sale = SaleService.create_sale(
                vehicle=vehicle,
                items_data=serializer.validated_data['items'],
                user=request.user,
                request=request,
            )
        except ValueError as e:
            raise ERPBusinessError(str(e), code='SAL_001')

        return Response(SaleDetailSerializer(sale).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get sale items."""
        sale = self.get_object()
        items = sale.items.select_related('item', 'vehicle_item').all()
        from .serializers import SaleItemSerializer
        return Response(SaleItemSerializer(items, many=True).data)

    def perform_destroy(self, instance):
        """Prevent deletion - use credit note for reversal."""
        raise ERPBusinessError(
            "Sales invoices cannot be deleted. Create a credit note to reverse.",
            code='SAL_001',
        )


class CreditNoteViewSet(viewsets.ModelViewSet):
    """Credit note management."""
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['party', 'status', 'financial_year', 'credit_note_date']
    search_fields = ['credit_note_number', 'party__party_name', 'sale__invoice_number']
    ordering_fields = ['credit_note_date', 'created_at']
    ordering = ['-credit_note_date']

    def get_queryset(self):
        company_id = self.request.session.get('company_id')
        qs = CreditNote.objects.select_related('party', 'sale', 'vehicle', 'created_by').prefetch_related('items')
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return CreditNoteListSerializer
        elif self.action == 'retrieve':
            return CreditNoteDetailSerializer
        elif self.action == 'create':
            return CreditNoteCreateSerializer
        return CreditNoteListSerializer

    def create(self, request, *args, **kwargs):
        """Create credit note to reverse a sale."""
        serializer = CreditNoteCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        sale_id = serializer.validated_data['sale_id']
        items_data = serializer.validated_data['items']
        reason = serializer.validated_data.get('reason', '')

        try:
            credit_note = SaleService.create_credit_note(
                sale_id=sale_id,
                items_data=items_data,
                user=request.user,
                reason=reason,
                request=request,
            )
        except ValueError as e:
            raise ERPBusinessError(str(e), code='SAL_001')

        return Response(
            CreditNoteDetailSerializer(credit_note).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['get'])
    def items(self, request, pk=None):
        """Get credit note items."""
        cn = self.get_object()
        items = cn.items.select_related('item', 'sale_item').all()
        from .serializers import CreditNoteItemSerializer
        return Response(CreditNoteItemSerializer(items, many=True).data)

    def perform_destroy(self, instance):
        raise ERPBusinessError(
            "Credit notes cannot be deleted.",
            code='SAL_001',
        )
