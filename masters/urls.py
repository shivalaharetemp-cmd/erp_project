from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'parties', views.PartyViewSet, basename='party')
router.register(r'items', views.ItemViewSet, basename='item')
router.register(r'transporters', views.TransporterViewSet, basename='transporter')
router.register(r'purchase-orders', views.PurchaseOrderViewSet, basename='purchase-order')

urlpatterns = router.urls
