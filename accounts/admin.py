from django.contrib import admin
from .models import CustomUser, MentorProfile, MenteeProfile, InvitationToken
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'is_mentor', 'mentor', 'created_at', 'updated_at']




@admin.register(MentorProfile)
class MentorProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'get_bio', 'get_profile_picture')
    

    @admin.display(description='Mentor Email', empty_value='-')
    def user_email(self, obj):
        return obj.user.email

    @admin.display(description='Bio Summary', empty_value='-')
    def get_bio(self, obj):
        return (obj.bio[:75] + '...') if obj.bio and len(obj.bio) > 75 else obj.bio
    
    @admin.display(description='Profile Picture')
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return '-'




@admin.register(MenteeProfile)
class MenteeProfileAdmin(admin.ModelAdmin):
    list_display = ('user_email', 'stage', 'created_at', 'get_profile_picture')


    @admin.display(description='Mentee Email', empty_value='-')
    def user_email(self, obj):
        return obj.user.email
    

    @admin.display(description='Profile Picture')
    def get_profile_picture(self, obj):
        if obj.profile_picture:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 50%;" />',
                obj.profile_picture.url
            )
        return '-'





@admin.register(InvitationToken)
class InvitationTokenAdmin(admin.ModelAdmin):
    list_display = ('token', 'mentee_email', 'mentor_email', 'expires_at', 'is_used', 'created_at')


    @admin.display(description='Inviting Mentor Email', empty_value='-')
    def mentor_email(self, obj):
        return obj.mentor.email
   

