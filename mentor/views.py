from django.shortcuts import render, redirect
from accounts.models import MenteeProfile
from django.http import HttpResponse





def dashboard_mentor(request):
    if request.user.is_authenticated:
        if request.user.is_mentor == True:
            my_mentees = MenteeProfile.objects.filter(user__mentor=request.user)
            total_mentees = my_mentees.count()
            active_mentees = total_mentees

            context = {
                'my_mentees':my_mentees, 
                'total_mentees':total_mentees,
            }

            return render(request, 'dashboard_mentor.html', context)
    
        else:
            return HttpResponse('You are not MENTOR.')
    else:
        return redirect('login')


    


    



