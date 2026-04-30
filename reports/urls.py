from django.urls import path
from . import views

urlpatterns = [
    path('ledger/', views.ledger_report, name='ledger_report'),
    path('stock/', views.stock_report, name='stock_report'),
    path('workflow/', views.workflow_report, name='workflow_report'),
    path('vouchers/', views.voucher_report, name='voucher_report'),
    path('financial/', views.financial_summary, name='financial_summary'),
    path('vehicles/', views.vehicle_report, name='vehicle_report'),
    path('companies/', views.company_summary, name='company_summary'),
]
