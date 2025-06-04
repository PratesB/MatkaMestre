from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import MenteeProfile, MentorProfile
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from .models import MentorAvailability, Task, MeetingRecording
from django.utils import timezone
from django.db import transaction



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





@login_required(redirect_field_name='login')
@require_http_methods(['GET','POST'])
def set_availability(request):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can set availability.')
        return redirect('login')
    
    
    
    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if not start_time or not end_time:
            messages.error(request, 'Start time and end time are required.')
            return render(request, 'set_availability.html')
        

        try:
            start = timezone.datetime.fromisoformat(start_time)
            end = timezone.datetime.fromisoformat(end_time)


            if end <= start:
                messages.error(request, 'End time must be after start time.')
                return render(request, 'set_availability.html')
            
            if start < timezone.now():
                messages.error(request, 'Start time cannot be in the past.')
                return render(request, 'set_availability.html')
            

            conflict_date = MentorAvailability.objects.filter(
                mentor = request.user.mentor_profile,
                start_time__lt = end,
                end_time__gt = start
            ).exists()

            if conflict_date:
                messages.error(request, 'This time slot conflicts with an existing availability.')
                return render(request, 'set_availability.html')
            

            with transaction.atomic():
                MentorAvailability.objects.create(
                    mentor = request.user.mentor_profile,
                    start_time=start,
                    end_time=end
                )

            messages.success(request, 'Availability slot added successfully!')
            return redirect('availability_list')
        
        except ValueError:
            messages.error(request, 'Invalid date or time format.')
            return render(request, 'set_availability.html')


    else:
        return render(request, 'set_availability.html', {'current_timezone': timezone.get_current_timezone_name()})
        




@login_required(redirect_field_name='login')
@require_http_methods(['GET'])
def availability_list(request):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can list availability.')
        return redirect('login')
    
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)

    slots = MentorAvailability.objects.filter(mentor=mentor_profile).order_by('start_time')


    context = {
        'mentor_profile': mentor_profile,
        'slots': slots,
    }
    
    return render(request, 'availability_list.html', context)





@login_required(redirect_field_name='login')
@require_http_methods(['GET', 'POST'])
def delete_availability(request, pk):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can delete availability.')
        return redirect('login')
    

    try:
        slot = get_object_or_404(MentorAvailability, id=pk, mentor=request.user.mentor_profile)

    except Exception:
        messages.error(request, 'Slot not found.')
        return redirect('availability_list')


    if slot.is_booked:
        messages.error(request, 'Cannot delete a booked slot.')
        return redirect('availability_list')


    try:
        with transaction.atomic():
            slot.delete()
            messages.success(request, 'Availability slot deleted successfully!')
            return redirect('availability_list')
    
    except Exception:
        messages.error(request, 'Error while delete the time.')
        return redirect('availability_list')
    
    



@login_required(redirect_field_name='login')
@require_http_methods(['GET','POST'])
def edit_availability(request, pk):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can edit availability.')
        return redirect('login')
    

    try:
        slot = get_object_or_404(MentorAvailability, id=pk, mentor=request.user.mentor_profile)

    
    except Exception:
        messages.error(request, 'Slot not found.')
        return redirect('availability_list')
    

    if slot.is_booked:
        messages.error(request, 'Cannot edit a booked slot.')
        return redirect('availability_list')
    

    context = {
        'slot': slot,
        'current_timezone': timezone.get_current_timezone_name(),
    }
    


    if request.method == 'POST':
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')

        if not start_time or not end_time:
            messages.error(request, 'Start time and end time are required.')
            return render(request, 'edit_availability.html', context)
        

        try:
            start = timezone.datetime.fromisoformat(start_time)
            end = timezone.datetime.fromisoformat(end_time)


            if end <= start:
                messages.error(request, 'End time must be after start time.')
                return render(request, 'edit_availability.html', context)
            
            if start < timezone.now():
                messages.error(request, 'Start time cannot be in the past.')
                return render(request, 'edit_availability.html', context)
            

            conflict_date = MentorAvailability.objects.filter(
                mentor = request.user.mentor_profile,
                start_time__lt = end,
                end_time__gt = start
            ).exclude(pk=slot.pk)

            if conflict_date:
                messages.error(request, 'This time slot conflicts with an existing availability.')
                return render(request, 'edit_availability.html', context)
            

            with transaction.atomic():
                slot.start_time = start
                slot.end_time = end
                slot.save()

            messages.success(request, 'Availability slot updated successfully!')
            return redirect('availability_list')
        
        except ValueError:
            messages.error(request, 'Invalid date or time format.')
            return render(request, 'edit_availability.html', context)


    else:
        return render(request, 'edit_availability.html', context)





@login_required(redirect_field_name='login')
@require_http_methods(['GET', 'POST'])
def create_task(request):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can create tasks.')
        return redirect('login')
    
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)
    
    my_mentees = MenteeProfile.objects.filter(user__mentor=request.user)

    context = {
        'my_mentees': my_mentees,
    }

    if request.method == 'POST':
        mentee_email = request.POST.get('mentee_email')
        description = request.POST.get('description')
        due_date_str = request.POST.get('due_date')
        
        if not all([mentee_email, description]):
            messages.error(request, 'Mentee and description are required.')
            return render(request, 'create_task.html', context)
        
        try:
            mentee_profile = get_object_or_404(MenteeProfile, user__email=mentee_email)
            

            if not mentor_profile: 
                messages.error(request, 'Selected mentee is not associated with your profile.')
                return render(request, 'create_task.html', context)


            due_date = None
            if due_date_str:
                due_date = timezone.datetime.fromisoformat(due_date_str)
                if due_date < timezone.now():
                    messages.error(request, 'Due date cannot be in the past.')
                    return render(request, 'create_task.html', context)
            
            with transaction.atomic():
                Task.objects.create(
                    mentor=mentor_profile,
                    mentee=mentee_profile,
                    description=description,
                    due_date=due_date
                )
            messages.success(request, 'Task created successfully!')
            return redirect('list_task')
        
        except ValueError:
            messages.error(request, 'Invalid date format for due date.')
            return render(request, 'create_task.html', context)
        except Exception:
            messages.error(request, 'An unexpected error occurred. Try again later.')
            return render(request, 'create_task.html', context)

    return render(request, 'create_task.html', context)




@login_required(redirect_field_name='login')
@require_http_methods(['GET'])
def list_task(request):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can create tasks.')
        return redirect('login')
    
    
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)
    
    tasks = Task.objects.filter(mentor = mentor_profile).order_by('due_date')

    return render(request, 'list_task.html', {'tasks':tasks})




@login_required(redirect_field_name='login')
@require_http_methods(['POST'])
def delete_task(request, pk):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can create tasks.')
        return redirect('login')
    
    
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)
    
    task = get_object_or_404(Task, mentor=mentor_profile, pk=pk)
    
    try:
        with transaction.atomic():
            task.delete()
        messages.success(request, 'Task deleted successfully!')
        return redirect('list_task')

    except Exception:
        messages.error(request, 'An error occurred while deleting the task. Try again later.')
        return redirect('list_task')


@login_required(redirect_field_name='login')
@require_http_methods(['POST'])
def toggle_task_status(request, pk):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can update task status.')
        return redirect('login')
    
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)
    
    task = get_object_or_404(Task, mentor=mentor_profile, pk=pk)
    
    try:
        with transaction.atomic():
            task.is_done = not task.is_done
            task.save()
        messages.success(request, 'Task status updated successfully!')
        return redirect('list_task')
    except Exception as e:
        messages.error(request, f'An error occurred while updating task status. Please, try again later.')
        return redirect('list_task')
    



@login_required(redirect_field_name='login')
@require_http_methods(['GET', 'POST'])
def edit_task(request, pk):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can create tasks.')
        return redirect('login')
    
    mentor_profile = get_object_or_404(MentorProfile, user=request.user)

    task = get_object_or_404(Task, mentor=mentor_profile, pk=pk)

    context = {
        'task': task,
    }

    if request.method == 'POST':
        description = request.POST.get('description')
        due_date_str = request.POST.get('due_date')


        
        if not description:
            messages.error(request, 'Description are required.')
            return render(request, 'edit_task.html', context)
        
        try:
            due_date = None
            if due_date_str:
                due_date = timezone.datetime.fromisoformat(due_date_str)
                if due_date < timezone.now():
                    messages.error(request, 'Due date cannot be in the past.')
                    return render(request, 'edit_task.html', context)
            
            with transaction.atomic():
                task.description = description
                task.due_date = due_date
                task.save()
            messages.success(request, 'Task updated successfully!')
            return redirect('list_task')
        
        except ValueError:
            messages.error(request, 'Invalid date format for due date.')
            return render(request, 'edit_task.html', context)
        except Exception as e:
            messages.error(request, f'An unexpected error occurred. Try again later.{e}')
            return render(request, 'edit_task.html', context)

    return render(request, 'edit_task.html', context)
    




@login_required(redirect_field_name='login')
@require_http_methods(['GET', 'POST'])
def upload_meeting_recording(request):
    if not request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentors can create tasks.')
        return redirect('login')
    

    mentor_profile = get_object_or_404(MentorProfile, user=request.user)


    my_mentees = MenteeProfile.objects.filter(user__mentor=request.user)


    context = {
        'my_mentees': my_mentees,
    }


  
    if request.method == 'POST':
        mentee_email = request.POST.get('mentee_email')
        title = request.POST.get('title')
        video = request.FILES.get('video')
        
        if not all([mentee_email, title, video]):
            messages.error(request, 'Mentee, title and description are required.')
            return render(request, 'upload_meeting_recording.html', context)
        
        try:
            mentee_profile = get_object_or_404(MenteeProfile, user__email=mentee_email)
            

            if not mentor_profile: 
                messages.error(request, 'Selected mentee is not associated with your profile.')
                return render(request, 'upload_meeting_recording.html', context)


            with transaction.atomic():
                MeetingRecording.objects.create(
                    mentor=mentor_profile,
                    mentee=mentee_profile,
                    title=title,
                    video=video,
                )
            messages.success(request, 'Meeting recording uploaded successfully!')
            return redirect('list_meeting_recordings')
        

        except Exception as e:
            messages.error(request, 'An unexpected error occurred during upload. Try again later.')
            return render(request, 'upload_meeting_recording.html', context)

    return render(request, 'upload_meeting_recording.html', context)





@login_required(redirect_field_name='login')
@require_http_methods(['GET'])
def list_meeting_recordings(request):    

    if request.user.is_mentor:
        mentor_profile = get_object_or_404(MentorProfile, user=request.user)        
        recordings = MeetingRecording.objects.filter(mentor=mentor_profile).order_by('mentee', '-uploaded_at')

        context = {
        'recordings': recordings,
        'is_mentor': request.user.is_mentor,
        }
        
    elif request.user.is_mentee:
        mentee_profile = get_object_or_404(MenteeProfile, user=request.user)
        recordings = MeetingRecording.objects.filter(mentee=mentee_profile).order_by('mentee', '-uploaded_at')

        context = {
        'recordings': recordings,
        'is_mentee': request.user.is_mentee,
        }

    else:
        messages.error(request, 'Access denied. You must be a mentor or mentee to view recordings.')
        return redirect('login') 

    
    return render(request, 'list_meeting_recordings.html', context)
