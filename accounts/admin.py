from django.contrib import admin
from .models import CustomUser, MentorProfile, MenteeProfile, InvitationToken
from django.contrib.auth.admin import UserAdmin


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_mentor', 'mentor', 'created_at', 'updated_at']




@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'get_bio')
    

    @admin.display(description='Mentor Email', empty_value='-')
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description='Bio Summary', empty_value='-')
    def get_bio(self, obj):
        return (obj.bio[:75] + '...') if obj.bio and len(obj.bio) > 75 else obj.bio




@admin.register(MenteeProfile)
class MenteeProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'stage', 'created_at')


    @admin.display(description='Mentee Email', empty_value='-')
    def user_email(self, obj):
        return obj.user.email





@admin.register(InvitationToken)
class InvitationTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'mentee_email', 'mentor_email', 'expires_at', 'is_used', 'created_at')


    @admin.display(description='Inviting Mentor Email', empty_value='-')
    def mentor_email(self, obj):
        return obj.mentor.email
   

