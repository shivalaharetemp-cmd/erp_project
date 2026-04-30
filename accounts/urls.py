# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # MasterGroup URLs
    path('groups/', views.MasterGroupListView.as_view(), name='mastergroup_list'),
    path('groups/create/', views.MasterGroupCreateView.as_view(), name='mastergroup_create'),
    path('groups/<int:pk>/', views.MasterGroupDetailView.as_view(), name='mastergroup_detail'),
    path('groups/<int:pk>/update/', views.MasterGroupUpdateView.as_view(), name='mastergroup_update'),
    path('groups/<int:pk>/delete/', views.MasterGroupDeleteView.as_view(), name='mastergroup_delete'),
    
    # Ledger URLs
    path('ledgers/', views.LedgerListView.as_view(), name='ledger_list'),
    path('ledgers/create/', views.LedgerCreateView.as_view(), name='ledger_create'),
    path('ledgers/<int:pk>/', views.LedgerDetailView.as_view(), name='ledger_detail'),
    path('ledgers/<int:pk>/update/', views.LedgerUpdateView.as_view(), name='ledger_update'),
    path('ledgers/<int:pk>/delete/', views.LedgerDeleteView.as_view(), name='ledger_delete'),
    
    # Voucher URLs
    path('vouchers/', views.VoucherListView.as_view(), name='voucher_list'),
    path('vouchers/create/', views.VoucherCreateView.as_view(), name='voucher_create'),
    path('vouchers/<int:pk>/', views.VoucherDetailView.as_view(), name='voucher_detail'),
    path('vouchers/<int:pk>/update/', views.VoucherUpdateView.as_view(), name='voucher_update'),
    path('vouchers/<int:pk>/delete/', views.VoucherDeleteView.as_view(), name='voucher_delete'),
]
