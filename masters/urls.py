# masters/urls.py
from django.urls import path
from . import views

urlpatterns = [
    # MasterType URLs
    path('types/', views.MasterTypeListView.as_view(), name='master_type_list'),
    path('types/create/', views.MasterTypeCreateView.as_view(), name='master_type_create'),
    path('types/<int:pk>/', views.MasterTypeDetailView.as_view(), name='master_type_detail'),
    path('types/<int:pk>/update/', views.MasterTypeUpdateView.as_view(), name='master_type_update'),
    path('types/<int:pk>/delete/', views.MasterTypeDeleteView.as_view(), name='master_type_delete'),
    
    # Master URLs
    path('', views.MasterListView.as_view(), name='master_list'),
    path('create/', views.MasterCreateView.as_view(), name='master_create'),
    path('<int:pk>/', views.MasterDetailView.as_view(), name='master_detail'),
    path('<int:pk>/update/', views.MasterUpdateView.as_view(), name='master_update'),
    path('<int:pk>/delete/', views.MasterDeleteView.as_view(), name='master_delete'),
]
