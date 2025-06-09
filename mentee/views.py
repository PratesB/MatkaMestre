from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from accounts.models import MenteeProfile, CustomUser
from mentor.models import Task, MentorAvailability, MeetingRecording
from django.utils import timezone




@login_required(redirect_field_name='login')
@require_http_methods(['GET'])
def dashboard_mentee(request):
    if request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentees can have access this page.')
        return redirect('login') 

    # Get mentee
    mentee_profile = get_object_or_404(MenteeProfile, user=request.user)
    if not mentee_profile:
        messages.error(request, 'Mentee not found.')
        return redirect('login')


    # Tasks
    tasks = Task.objects.filter(mentee = mentee_profile).order_by('due_date')
    completed_tasks_count = tasks.filter(is_done=True).count()
    pending_tasks_count = tasks.filter(is_done=False).count()



    # Availability Times
    available_slots = []
    if request.user.mentor:
        try:
            mentor_profile = request.user.mentor.mentor_profile
            available_slots = MentorAvailability.objects.filter(
                mentor=mentor_profile,
                is_booked=False,
                start_time__gte=timezone.now()
            ).order_by('start_time')
        except CustomUser.mentor_profile.RelatedObjectDoesNotExist:
            messages.warning(request, 'Mentor profile not found. Contact your mentor.')


    # Reserved Slots
    reserved_slots = []
    if mentor_profile:
        reserved_slots = MentorAvailability.objects.filter(
            mentee=mentee_profile,
            mentor=mentor_profile,
            is_booked=True,
            start_time__gte=timezone.now()
        ).order_by('start_time')



    # Meeting recordings
    recordings = MeetingRecording.objects.filter(mentee=mentee_profile).order_by('-uploaded_at')

    


    context = {
        'tasks': tasks,
        'completed_tasks_count': completed_tasks_count,
        'pending_tasks_count': pending_tasks_count,
        'available_slots': available_slots,
        'recordings': recordings,
        'is_mentor': False,
        'reserved_slots': reserved_slots,
        'mentor_profile': mentor_profile,
        'mentee_profile': mentee_profile,
    }
    
    

    return render(request, 'dashboard_mentee.html', context)





@login_required
@require_http_methods(['POST'])
def complete_task(request, task_id):
    if request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentees can have access this page.')
        return redirect('login')
    
    try:
        mentee_profile = request.user.mentee_profile

    except CustomUser.mentee_profile.RelatedObjectDoesNotExist:
        messages.error(request, 'Mentee profile not found. Please complete your profile.')
        return redirect('login')

    task = get_object_or_404(Task, id=task_id, mentee=mentee_profile, is_done=False)
    task.is_done = True
    task.save()

    messages.success(request, 'Task marked as completed successfully!')
    return redirect('dashboard_mentee')



@login_required
@require_http_methods(['POST'])
def book_slot(request, slot_id):
    if request.user.is_mentor:
        messages.error(request, 'Access denied. Only mentees can have access this page.')
        return redirect('login')
    
    try:
        mentee_profile = request.user.mentee_profile

    except CustomUser.mentee_profile.RelatedObjectDoesNotExist:
        messages.error(request, 'Mentee profile not found. Please complete your profile.')
        return redirect('login')
    

    try:
        mentor_profile = request.user.mentor.mentor_profile

    except CustomUser.mentor_profile.RelatedObjectDoesNotExist:
        messages.error(request, 'Mentor profile not found. Contact your mentor.')
        return redirect('dashboard_mentee')
    

    slot = get_object_or_404(
        MentorAvailability, 
        id=slot_id, 
        mentor = mentor_profile, 
        is_booked = False, 
        start_time__gte=timezone.now()
    )

    
    slot.is_booked = True
    slot.mentee = mentee_profile
    slot.save()

    messages.success(request, 'Time slot booked successfully!')
    return redirect('dashboard_mentee')


