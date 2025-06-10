from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_mentee/', views.dashboard_mentee, name='dashboard_mentee'),
    path('complete_task/<int:task_id>', views.complete_task, name='complete_task'),
    path('book_slot/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('mentee_profile/<int:mentee_id>/', views.mentee_profile, name='mentee_profile'),
    
]