from django.db import models
from accounts.models import MentorProfile, MenteeProfile



class MentorAvailability(models.Model):
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)



class Task(models.Model):
    mentor = models.ForeignKey(MentorProfile, on_delete=models.CASCADE)
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(blank=True, null=True)



class MeetingRecording(models.Model):
    mentor = models.ForeignKey(MentorProfile, on_delete=models.SET_NULL, null=True, blank=True)
    mentee = models.ForeignKey(MenteeProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    video = models.FileField(upload_to='video')
    uploaded_at = models.DateTimeField(auto_now_add=True)





