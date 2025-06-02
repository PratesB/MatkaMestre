from django.urls import path
from . import views
    


urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'), 
    path('invite_mentee/', views.invite_mentee, name='invite_mentee'), 
    path('register_mentee/', views.register_mentee, name='register_mentee'),

]
