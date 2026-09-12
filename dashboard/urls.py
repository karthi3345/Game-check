from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('providers/', views.provider_list, name='provider_list'),
    path('providers/<int:pk>/', views.provider_detail, name='provider_detail'),
    path('history/', views.test_history, name='test_history'),
]
