from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    email=models.EmailField(max_length=254, unique=True)
    is_mentor = models.BooleanField(default=False)
    mentor = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'Email: {self.email} | Is Mentor: {self.is_mentor} | Created at: {self.created_at}'





class MentorProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mentor_profile')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'Mentor profile of {self.user.email}'
    


class MenteeProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='mentee_profile')
    stage = models.CharField(
        max_length=50,
        choices=[
            ('1k-10k', '1k-10k'),
            ('10k-100k', '10k-100k'),
            ('100k+', '100k+')
        ]
    )


    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Mentee profile of {self.user.email}'
    



class InvitationToken(models.Model):
    token = models.CharField(max_length=100, unique=True)
    mentee_email = models.EmailField(max_length=254)
    mentor = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    is_used = models.BooleanField(default=False)

    def __str__(self):
        return f'Token for {self.mentee_email} by {self.mentor.email}'