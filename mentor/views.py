from django.shortcuts import render, redirect
from accounts.models import MenteeProfile
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required




@login_required(redirect_field_name='login')
def dashboard_mentor(request):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can view this dashboard.')
        return redirect('login')

    my_mentees = MenteeProfile.objects.filter(user__mentor=request.user)
    total_mentees = my_mentees.count()

    context = {
        'my_mentees': my_mentees,
        'total_mentees': total_mentees,
    }

    return render(request, 'dashboard_mentor.html', context)



    


    



