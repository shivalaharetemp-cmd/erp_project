from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('core.urls')),
    path('api/company/', include('core.company_urls')),
    path('api/masters/', include('masters.urls')),
    path('api/vehicles/', include('vehicles.urls')),
    path('api/freight/', include('freight.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/audit/', include('audit.urls')),
]

# Custom admin title
admin.site.site_header = 'ERP Admin'
admin.site.site_title = 'ERP Administration'
admin.site.index_title = 'Dashboard'
