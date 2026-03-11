from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.task_list, name='task_list'),
    path('nueva/', views.task_create, name='task_create'),
    path('editar/<int:pk>/', views.task_edit, name='task_edit'),
    path('eliminar/<int:pk>/', views.task_delete, name='task_delete'),
]