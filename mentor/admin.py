from django.contrib import admin
from .models import MentorAvailability, Task, MeetingRecording



@admin.register(MentorAvailability)
class MentorAvailabilityAdmin(admin.ModelAdmin):
    list_display = ['mentor_email', 'start_time', 'end_time', 'is_booked', 'mentee']
    readonly_fields = ('start_time', 'end_time')
    ordering = ('start_time',)

    
    @admin.display(description='Mentor Email', empty_value='-')
    def mentor_email(self, obj):
        return obj.mentor.user.email
    
    
    





@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ['mentor_email', 'mentee_email', 'title', 'description', 'is_done', 'created_at', 'due_date']
    readonly_fields = ('created_at', 'due_date')
    ordering = ('-created_at',)

    
    @admin.display(description='Mentor Email', empty_value='-')
    def mentor_email(self, obj):
        return obj.mentor.user.email
    
    
    @admin.display(description='Mentee Email', empty_value='-')
    def mentee_email(self, obj):
        return obj.mentee.user.email
    



@admin.register(MeetingRecording)
class MeetingRecordingAdmin(admin.ModelAdmin):
    list_display = ['mentor_email','title', 'mentee_email', 'video', 'uploaded_at']
    readonly_fields = ('uploaded_at',)
    ordering = ('-uploaded_at',)

    
    @admin.display(description='Mentor Email', empty_value='-')
    def mentor_email(self, obj):
        return obj.mentor.user.email if obj.mentor and obj.mentor.user else '-'
    
    
    
    @admin.display(description='Mentee Email', empty_value='-')
    def mentee_email(self, obj):
        return obj.mentee.user.email if obj.mentee and obj.mentee.user else '-'