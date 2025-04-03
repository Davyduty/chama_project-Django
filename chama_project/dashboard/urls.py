from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.dashboard_home, name='home'),
    path('admin/', views.admin_dashboard, name='admin'),
    path('admin/loans/', views.admin_loans, name='admin_loans'),
    path('user/<int:user_id>/', views.user_details, name='user_details'),
]

