from django.urls import path
from . import views
    


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'), 
    path('invite_mentee/', views.invite_mentee, name='invite_mentee'), 
    path('register_mentee/', views.register_mentee, name='register_mentee'),
    path('update_mentorprofile/', views.update_mentorprofile, name='update_mentorprofile'),
    path('delete_mentee/<int:user_id>', views.delete_mentee, name='delete_mentee'),
    path('delete_mentor/<int:user_id>', views.delete_mentor, name='delete_mentor'),
    path('update_menteeprofile/', views.update_menteeprofile, name='update_menteeprofile'),

]
