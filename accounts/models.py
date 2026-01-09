from django.db import models
from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, blank=True)
    gender = models.CharField(max_length=10, choices=[('MALE', 'Male'), ('FEMALE', 'Female'), ('OTHER', 'Other')], blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    location = models.CharField(max_length=255, blank=True)
    alternate_mobile = models.CharField(max_length=15, blank=True)
    hint_name = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'Profile for {self.user.username}'