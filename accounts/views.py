from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser, MentorProfile, MenteeProfile, InvitationToken
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login as login_django, logout as logout_django, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from uuid import uuid4
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction
from django.contrib.auth.hashers import make_password
from mentor.models import MentorAvailability



@require_http_methods(['GET','POST'])
def register(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_mentor:
                return redirect('dashboard_mentor')
            else:
                return redirect('dashboard_mentee')
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
        

        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_mentor=True
        )

        MentorProfile.objects.create(user=user)

        messages.success(request, 'Account created successfully!')
        return redirect('login')





@require_http_methods(['GET', 'POST'])
def login(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            if request.user.is_mentor == True:
                return redirect('dashboard_mentor')
            if request.user.is_mentor == False:
                return redirect('dashboard_mentee')
        return render(request, 'login.html')
    

    else:
        email = request.POST.get('email')
        password = request.POST.get('password')


        user = authenticate(username=email, password=password)

        if user:
            login_django(request, user)

            if user.is_mentor:
                return redirect('dashboard_mentor')
            else:
                return redirect('dashboard_mentee')


        else:
            messages.error(request, 'Email or password invalid.')
            return redirect('login')




@login_required(redirect_field_name='home')
@require_http_methods(['GET'])
def logout(request):
    logout_django(request)
    return redirect('home')





@require_http_methods(['GET','POST'])
def invite_mentee(request):
    if not request.user.is_authenticated or not request.user.is_mentor:
        messages.error(request, 'Only mentor can invite mentee.')
        return redirect('login')
        

    if request.method == 'POST':
        mentee_email = request.POST.get('mentee_email')


        if CustomUser.objects.filter(email=mentee_email).exists():
            messages.error(request, 'This mentee mail is already used.')
            return render(request, 'invite_mentee.html')


        
        if InvitationToken.objects.filter(mentee_email=mentee_email, is_used = False, expires_at__gt=timezone.now()).exists():
            messages.error(request, f'There is already an active invitation for this email: {mentee_email}.')
            return render(request, 'invite_mentee.html')


        token = str(uuid4())

        try:
            InvitationToken.objects.create(
                token = token,
                mentee_email = mentee_email,
                mentor = request.user,
                expires_at = timezone.now() + timedelta(hours=24),

            )

            invite_url = request.build_absolute_uri(f'/accounts/register_mentee/?token={token}')


            send_mail(
                subject='Invite to join MatkaMestre',
                message=f'Hello!\n\n You have been invited by {request.user.email} to join MatkaMestre as a mentee. Use this link to register:{invite_url}\n\nImportant: this invite link is valid for 24 hours.\n\nKind regards,\n\nMatkaMestre Team.',

                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[mentee_email],
                fail_silently=False,
            )


            messages.success(request, f'Invitation sent successfully to:{mentee_email}')
            return redirect('dashboard_mentor')

        except Exception as e:
            messages.error(request, f'An error occurred while sending the invitation. Please try again later.')
            return redirect('invite_mentee')


    return render(request, 'invite_mentee.html')
        





@require_http_methods(['GET','POST'])
def register_mentee(request):

    token = request.GET.get('token') if request.method=='GET' else request.POST.get('token')


    if not token:
        messages.error(request, 'Invitation token is invalid or missing.')
        return render(request, 'register_mentee.html')
    

    try:
        invitation = InvitationToken.objects.get(token=token)
        if invitation.is_used or invitation.expires_at < timezone.now():
            messages.error(request, 'This invitation link is invalid or has expired.')
            return render(request, 'register_mentee.html')
        
    except InvitationToken.DoesNotExist:
        messages.error(request, 'This invitation token was not found.')
        return render(request, 'register_mentee.html')
    
    context = {
            'token':token,
            'mentee_email': invitation.mentee_email
        }
    



    if request.method == 'GET':      
        return render(request, 'register_mentee.html', context)
    


    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        stage = request.POST.get('stage')


        if confirm_password != password:
            messages.error(request, 'Your passwords do not match. Please, try again.')
            return render(request, 'register_mentee.html', context)
        

        if len(password) < 6:
            messages.error(request, 'Your password needs to be 6 characters or more.')
            return render(request, 'register_mentee.html', context)
        

        if email != invitation.mentee_email:
            messages.error(request, 'The email provided does not match the invitation email.')
            return render(request, 'register_mentee.html', context)
        

        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'register_mentee.html', context)
        


        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'This email is already used.')
            return render(request, 'register_mentee.html', context)
        

        try:

            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                is_mentor= False,
                mentor=invitation.mentor
            )


            MenteeProfile.objects.create(
                user=user,
                stage=stage
            )

            invitation.is_used=True

            invitation.save()

            messages.success(request, 'Mentee account created successfully! Please log in.')
            return redirect('login')
    

        except Exception as e:
            messages.error(request, 'An unexpected error occurred. Please try again later.')
            return render(request, 'register_mentee.html', context)

    



@login_required(redirect_field_name='login')
@require_http_methods(['GET','POST'])
def update_mentorprofile(request):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can updated your profile.')
        return redirect('login')
    

    mentor_profile = MentorProfile.objects.filter(user=request.user).first()
    if not mentor_profile:
        mentor_profile = MentorProfile.objects.create(user=request.user)



    if request.method == 'GET':

        context = {
            'user_data': request.user,
            'profile_data': mentor_profile, 
        }

        return render(request, 'update_mentorprofile.html', context)
    
            
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password') 
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        bio = request.POST.get('bio')


        context = {
            'user_data': request.user,
            'profile_data': mentor_profile,
            'form_data':{
                'username': username,
                'email': email,
                'bio': bio,
            }
        }


        if not current_password:
            messages.error(request, 'Please, enter your current password to updated info.')
            return render(request, 'update_mentorprofile.html', context)
        

        if not request.user.check_password(current_password):
            messages.error(request, 'Your current password informed is incorrect.')
            return render(request, 'update_mentorprofile.html', context)
        

        if CustomUser.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'update_mentorprofile.html', context)
        
            
        if CustomUser.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            messages.error(request, 'This email is already used.')
            return render(request, 'update_mentorprofile.html', context)
        


        if new_password or confirm_password:          
            if confirm_password != new_password:
                messages.error(request, 'Your passwords do not match. Please, try again.')
                return render(request, 'update_mentorprofile.html', context)
        
            if len(new_password) < 6:
                messages.error(request, 'Your password needs to be 6 characters or more.')
                return render(request, 'update_mentorprofile.html', context)

        
        try:
            with transaction.atomic():         
                request.user.username = username
                request.user.email = email

                if new_password and confirm_password and new_password == confirm_password:
                    request.user.set_password(new_password)
                    messages.success(request, 'Your password was updated successfully!')

                request.user.save()

                if new_password and confirm_password and new_password == confirm_password:
                     update_session_auth_hash(request, request.user)


                mentor_profile.bio = bio
                mentor_profile.save()


                messages.success(request, 'Mentor profile updated successfully!')
                return render(request, 'update_mentorprofile.html', context)


        except Exception as e:
            messages.error(request, 'An unexpected error occurred. Please try again later.')
            return render(request, 'update_mentorprofile.html', context)

                



@login_required(redirect_field_name='login')
@require_http_methods(['GET','POST'])
def delete_mentee(request, user_id):

    user_to_delete = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        password = request.POST.get('password')


        if not request.user.check_password(password):
            messages.error(request, 'The password you entered is incorrect.')
            return render(request, 'delete_mentee.html', {'user_to_delete':user_to_delete})

        try:
            with transaction.atomic():
                try:
                    mentee_profile = user_to_delete.mentee_profile

                    slots = MentorAvailability.objects.filter(mentee=mentee_profile, is_booked=True)
                    slots.update(is_booked=False, mentee=None)

                    mentee_profile.delete()

                    if CustomUser.objects.filter(id=user_id).exists():
                        user_to_delete.delete()
                        

                except CustomUser.mentee_profile.RelatedObjectDoesNotExist:
                    messages.error(request, 'This user is not a mentee and can not be deleted.')
                    return render(request, 'delete_mentee.html', {'user_to_delete': user_to_delete})
                    


                messages.success(request, 'Mentee deleted successfully!')

                if request.user.is_mentor:
                    return redirect('dashboard_mentor')
                else:
                    return redirect('home')

            
        except Exception as e:
            messages.error(request, 'An error occurred while deleting the mentee. Try again later.')
            return render(request, 'delete_mentee.html', {'user_to_delete': user_to_delete})


    else:
        return render(request, 'delete_mentee.html', {'user_to_delete':user_to_delete})
    



@login_required(redirect_field_name='login')
@require_http_methods(['GET', 'POST'])
def delete_mentor(request, user_id):
    if request.user.id != user_id:
        messages.error(request, 'You do not have permission to delete this account.')
        return redirect('dashboard_mentor')

    user_to_delete = get_object_or_404(CustomUser, id=user_id)

    if request.method == 'POST':
        password = request.POST.get('password')

        if not request.user.check_password(password):
            messages.error(request, 'The password you entered is incorrect.')
            return render(request, 'delete_mentor.html', {'user_to_delete': user_to_delete})

        try:
            with transaction.atomic():
                user_to_delete.delete()
            messages.success(request, 'Your mentor account has been deleted successfully!')
            return redirect('home') 

        except Exception as e:
            messages.error(request, f'An error occurred while deleting the account.')
            return render(request, 'delete_mentor.html', {'user_to_delete': user_to_delete})

    else:
        return render(request, 'delete_mentor.html', {'user_to_delete': user_to_delete})




@login_required(redirect_field_name='login')
@require_http_methods(['GET','POST'])
def update_menteeprofile(request):
    if request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentees can updated your profile.')
        return redirect('login')
    

    mentee_profile = MenteeProfile.objects.filter(user=request.user).first()

    if not mentee_profile:
        mentee_profile = MentorProfile.objects.create(user=request.user)



    if request.method == 'GET':

        context = {
            'user_data': request.user,
            'mentee_profile': mentee_profile, 
        }

        return render(request, 'update_menteeprofile.html', context)
    
            
    else:
        username = request.POST.get('username')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password') 
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        stage = request.POST.get('stage')


        context = {
            'user_data': request.user,
            'mentee_profile': mentee_profile,
            'form_data':{
                'username': username,
                'email': email,
                'stage': stage,
            }
        }


        if not current_password:
            messages.error(request, 'Please, enter your current password to updated info.')
            return render(request, 'update_mentorprofile.html', context)
        

        if not request.user.check_password(current_password):
            messages.error(request, 'Your current password informed is incorrect.')
            return render(request, 'update_mentorprofile.html', context)
        

        if CustomUser.objects.filter(username=username).exclude(pk=request.user.pk).exists():
            messages.error(request, 'Username already exists. Please choose a different one.')
            return render(request, 'update_mentorprofile.html', context)
        
            
        if CustomUser.objects.filter(email=email).exclude(pk=request.user.pk).exists():
            messages.error(request, 'This email is already used.')
            return render(request, 'update_mentorprofile.html', context)
        


        if new_password or confirm_password:          
            if confirm_password != new_password:
                messages.error(request, 'Your passwords do not match. Please, try again.')
                return render(request, 'update_mentorprofile.html', context)
        
            if len(new_password) < 6:
                messages.error(request, 'Your password needs to be 6 characters or more.')
                return render(request, 'update_mentorprofile.html', context)

        
        try:
            with transaction.atomic():         
                request.user.username = username
                request.user.email = email
                

                if new_password and confirm_password and new_password == confirm_password:
                    request.user.set_password(new_password)
                    messages.success(request, 'Your password was updated successfully!')

                request.user.save()

                if new_password and confirm_password and new_password == confirm_password:
                     update_session_auth_hash(request, request.user)

                mentee_profile.stage = stage
                mentee_profile.save()

                messages.success(request, 'Mentee profile updated successfully!')
                return render(request, 'update_menteeprofile.html', context)


        except Exception as e:
            messages.error(request, 'An unexpected error occurred. Please try again later.')
            return render(request, 'update_menteeprofile.html', context)
