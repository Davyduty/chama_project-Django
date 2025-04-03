from django.urls import path
from . import views

app_name = 'contributions'

urlpatterns = [
    path('', views.contribution_list, name='list'),
    path('make/', views.make_contribution, name='make'),
    path('<int:pk>/', views.contribution_detail, name='detail'),
]

