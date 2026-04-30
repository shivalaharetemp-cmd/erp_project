# company/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='company_list'),
    path('create/', views.CompanyCreateView.as_view(), name='company_create'),
    path('<int:pk>/', views.CompanyDetailView.as_view(), name='company_detail'),
    path('<int:pk>/update/', views.CompanyUpdateView.as_view(), name='company_update'),
    path('<int:pk>/delete/', views.CompanyDeleteView.as_view(), name='company_delete'),
]
