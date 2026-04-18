from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'logs', views.AuditLogViewSet, basename='audit-log')

urlpatterns = router.urls
