from django.urls import path
from . import views

app_name = 'loans'

urlpatterns = [
    path('', views.loan_list, name='list'),
    path('apply/', views.loan_application, name='apply'),
    path('<int:pk>/', views.loan_detail, name='detail'),
    path('<int:pk>/update-status/', views.update_loan_status, name='update_status'),
]

