
from django.urls import path
from . import views

urlpatterns = [
    path('dashboard_mentor/', views.dashboard_mentor, name='dashboard_mentor'),
    path('set_availability/', views.set_availability, name='set_availability'),
    path('availability_list/', views.availability_list, name='availability_list'),
    path('delete_availability/<int:pk>', views.delete_availability, name='delete_availability'),
    path('edit_availability/<int:pk>', views.edit_availability, name='edit_availability'),
    path('create_task/', views.create_task, name='create_task'),
    path('list_task/', views.list_task, name='list_task'),
    path('delete_task/<int:pk>', views.delete_task, name='delete_task'),
    path('toggle_task_status/<int:pk>', views.toggle_task_status, name='toggle_task_status'),
    path('edit_task/<int:pk>', views.edit_task, name='edit_task'),
    path('upload_meeting_recording/', views.upload_meeting_recording, name='upload_meeting_recording'),
    path('list_meeting_recordings/', views.list_meeting_recordings, name='list_meeting_recordings'),
    path('mentor_profile/', views.mentor_profile, name='mentor_profile'),
]
