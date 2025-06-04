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
