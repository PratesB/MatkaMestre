from django.shortcuts import render, redirect
from .models import CustomUser, MentorProfile, MenteeProfile, InvitationToken
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout as logout_django
from django.contrib.auth.decorators import login_required




@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_mentor == True:
                return HttpResponse('dashboard_mentor')
                # TODO: return redirect('dashboard_mentor')
            if request.user.is_mentor == False:
                return HttpResponse('dashboard_mentee')
                # TODO: return redirect('dashboard_mentee')
        return render(request, 'register.html')
    

    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')



        if confirm_password != password:
            messages.error(request, 'Your passwords do not match. Please, try again.')
            return redirect('register')
        

        if len(password) < 6:
            messages.error(request, 'Your password needs to be 6 characters or more.')
            return redirect('register')
        

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return redirect('register')
        

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists. Please chose a different one.')
            return redirect('register')
        

        CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_mentor=True
        )

        messages.success(request, 'Account created successfully!')
        return redirect('login')





@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_mentor == True:
                return HttpResponse('dashboard_mentor')
                # TODO: return redirect('dashboard_mentor')
            if request.user.is_mentor == False:
                return HttpResponse('dashboard_mentee')
                # TODO: return redirect('dashboard_mentee')
        return render(request, 'login.html')
    

    else:
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = authenticate(username=email, password=password)

        if user:
            login_django(request, user)
            return HttpResponse('dashboard_mentor')
            # TODO: return redirect('dashboard_mentor')

        else:
            messages.error(request, 'Email or password invalid.')
            return redirect('login')



@login_required(redirect_field_name='home')
@require_http_methods(['POST'])
def logout(request):
    logout_django(request)
    return redirect('home')
