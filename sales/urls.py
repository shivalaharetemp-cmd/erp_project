from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'invoices', views.SaleViewSet, basename='sale')
router.register(r'credit-notes', views.CreditNoteViewSet, basename='credit-note')

urlpatterns = router.urls
