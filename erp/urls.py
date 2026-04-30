# erp/urls.py
from django.contrib import admin
from django.urls import path, include
from reports.views import ledger_report, stock_report, workflow_report

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('company/', include('company.urls')),
    path('masters/', include('masters.urls')),
    path('accounts/', include('accounts.urls')),
    path('inventory/', include('inventory.urls')),
    path('logistics/', include('logistics.urls')),
    path('workflow/', include('workflow.urls')),
    path('reports/', include('reports.urls')),
]