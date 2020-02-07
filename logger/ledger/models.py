from django.db import models
# from django.contrib.auth.models import User
import django.contrib.auth.hashers

class Member(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    email = models.EmailField(max_length=100, blank=False, null=False, default='defaultmail@domain.name', help_text="NISER Email of the User")
    hashed_secret_key = models.CharField(max_length=200, null=False, blank=False)
    login_count = models.IntegerField(default=0, help_text="Number of Logins by this user")
    is_active = models.BooleanField(default=False, help_text="Controls, if the user can login!")
    # OTP = models.CharField(max_length=6, help_text="DO NOT ALTER!")
    def __str__(self):
        return f'{self.name} ({self.email})'

import uuid
from datetime import datetime as dt
class MemberLoginInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Don\'t change! Unique ID for this particular login!')
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, help_text="User details")
    logged_out = models.BooleanField(default=True, help_text="If you are setting this to 'True', manually, please also fill in the 'logout_timestamp' field (Select 'Now')! Also, under no condition, set this to 'False', once set to 'True'!")
    login_timestamp = models.DateTimeField(null=True, blank=True, default=dt.now)
    logout_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['logout_timestamp']

    def __str__(self):
        return f'{self.id} ({self.member.name})'

