
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_mentor/', views.dashboard_mentor, name='dashboard_mentor'),
    path('set_availability/', views.set_availability, name='set_availability'),
    path('availability_list/', views.availability_list, name='availability_list'),
    path('delete_availability/<int:pk>', views.delete_availability, name='delete_availability'),
]
