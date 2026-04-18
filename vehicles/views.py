from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Vehicle, VehicleItem, VehicleChangeLog
from .serializers import (
    VehicleListSerializer, VehicleCreateSerializer, VehicleUpdateSerializer,
    VehicleLoadSerializer, VehicleCancelSerializer, VehicleChangeSerializer,
    VehicleItemSerializer, VehicleChangeLogSerializer,
)
from .services import VehicleService
from core.exceptions import ERPPermissionError, ERPBusinessError


class VehicleViewSet(viewsets.ModelViewSet):
    """Vehicle management with workflow actions."""
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status', 'transporter', 'party']
    search_fields = ['vehicle_number', 'party__party_name']
    ordering_fields = ['created_at', 'vehicle_number']
    ordering = ['-created_at']

    def get_queryset(self):
        company_id = self.request.session.get('company_id')
        qs = Vehicle.objects.select_related('transporter', 'party', 'created_by').prefetch_related('items', 'freights')
        if company_id:
            qs = qs.filter(company_id=company_id)
        return qs

    def get_serializer_class(self):
        if self.action == 'list':
            return VehicleListSerializer
        elif self.action == 'create':
            return VehicleCreateSerializer
        elif self.action in ('update', 'partial_update'):
            return VehicleUpdateSerializer
        elif self.action == 'load':
            return VehicleLoadSerializer
        elif self.action == 'cancel':
            return VehicleCancelSerializer
        elif self.action == 'change_vehicle_number':
            return VehicleChangeSerializer
        elif self.action == 'change_logs':
            return VehicleChangeLogSerializer
        elif self.action == 'items':
            return VehicleItemSerializer
        return VehicleListSerializer

    def perform_create(self, serializer):
        company_id = self.request.session.get('company_id')
        data = serializer.validated_data
        vehicle = VehicleService.create_vehicle(
            data=data,
            user=self.request.user,
            company_id=company_id,
            request=self.request,
        )
        serializer.instance = vehicle

    def perform_update(self, serializer):
        vehicle = serializer.instance
        if not vehicle.is_editable:
            raise ERPBusinessError(
                f"Vehicle with status '{vehicle.status}' cannot be edited.",
                code='VEH_001',
                details={'vehicle_id': str(vehicle.id), 'current_status': vehicle.status},
            )
        serializer.save()

    @action(detail=True, methods=['post'], url_path='load')
    def load(self, request, pk=None):
        """Load items onto a vehicle. Locks qty & vehicle number."""
        vehicle = self.get_object()
        serializer = VehicleLoadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            vehicle = VehicleService.load_vehicle(
                vehicle=vehicle,
                items_data=serializer.validated_data['items'],
                user=request.user,
                request=request,
            )
        except ValueError as e:
            raise ERPBusinessError(str(e), code='VEH_001')

        return Response(VehicleListSerializer(vehicle, context={'request': request}).data)

    @action(detail=True, methods=['post'], url_path='cancel')
    def cancel(self, request, pk=None):
        """Cancel a vehicle."""
        vehicle = self.get_object()
        serializer = VehicleCancelSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            vehicle = VehicleService.cancel_vehicle(
                vehicle=vehicle,
                reason=serializer.validated_data['reason'],
                user=request.user,
                request=request,
            )
        except ValueError as e:
            raise ERPBusinessError(str(e), code='VEH_001')

        return Response(VehicleListSerializer(vehicle, context={'request': request}).data)

    @action(detail=True, methods=['post'], url_path='change-vehicle')
    def change_vehicle_number(self, request, pk=None):
        """Change vehicle number with permission and audit."""
        vehicle = self.get_object()
        user = request.user

        # Permission check: only Admin or Manager can change vehicle
        if not user.has_role_permission(['admin', 'manager']):
            raise ERPPermissionError(
                "You don't have permission to change vehicle number.",
                code='PERM_001',
            )

        serializer = VehicleChangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            vehicle = VehicleService.change_vehicle(
                vehicle=vehicle,
                new_number=serializer.validated_data['new_vehicle_number'],
                reason=serializer.validated_data['reason'],
                user=user,
                request=request,
            )
        except ValueError as e:
            raise ERPBusinessError(str(e), code='VEH_001')

        return Response(VehicleListSerializer(vehicle, context={'request': request}).data)

    @action(detail=True, methods=['get'], url_path='change-logs')
    def change_logs(self, request, pk=None):
        """View vehicle change history."""
        vehicle = self.get_object()
        logs = vehicle.change_logs.all()
        serializer = VehicleChangeLogSerializer(logs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'], url_path='items')
    def items(self, request, pk=None):
        """View items loaded on a vehicle."""
        vehicle = self.get_object()
        items = vehicle.items.select_related('item').all()
        serializer = VehicleItemSerializer(items, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='po-rate')
    def po_rate(self, request):
        """Fetch PO rate for a party+item combination."""
        from masters.models import Party, Item
        party_id = request.query_params.get('party_id')
        item_id = request.query_params.get('item_id')

        if not party_id or not item_id:
            return Response({'error': 'party_id and item_id are required.'}, status=400)

        company_id = request.session.get('company_id')
        try:
            party = Party.objects.get(id=party_id, company_id=company_id)
            item = Item.objects.get(id=item_id, company_id=company_id)
        except (Party.DoesNotExist, Item.DoesNotExist):
            return Response({'error': 'Party or Item not found.'}, status=404)

        rate, po_number = VehicleService.get_po_rate(party, item, company_id)
        if rate:
            return Response({'rate': str(rate), 'po_number': po_number, 'source': 'PO Reference'})
        return Response({'rate': None, 'source': 'Manual (Verbal/Current Market)'})

    def perform_destroy(self, instance):
        """Prevent deletion - only cancellation allowed."""
        raise ERPBusinessError(
            "Vehicles cannot be deleted. Use the cancel endpoint instead.",
            code='VEH_001',
        )
