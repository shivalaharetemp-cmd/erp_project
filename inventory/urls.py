# inventory/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # Item URLs
    path('items/', views.ItemListView.as_view(), name='item_list'),
    path('items/create/', views.ItemCreateView.as_view(), name='item_create'),
    path('items/<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('items/<int:pk>/update/', views.ItemUpdateView.as_view(), name='item_update'),
    path('items/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item_delete'),
    
    # StockTransaction URLs
    path('transactions/', views.StockTransactionListView.as_view(), name='stocktransaction_list'),
    path('transactions/create/', views.StockTransactionCreateView.as_view(), name='stocktransaction_create'),
    path('transactions/<int:pk>/', views.StockTransactionDetailView.as_view(), name='stocktransaction_detail'),
    path('transactions/<int:pk>/update/', views.StockTransactionUpdateView.as_view(), name='stocktransaction_update'),
    path('transactions/<int:pk>/delete/', views.StockTransactionDeleteView.as_view(), name='stocktransaction_delete'),
]
