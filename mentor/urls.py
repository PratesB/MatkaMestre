
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_mentor/', views.dashboard_mentor, name='dashboard_mentor' )
]
