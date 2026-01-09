from django import forms
from django.contrib.auth import get_user_model
from .models import Profile


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=False, help_text="Used for order updates")

    class Meta:
        model = Profile
        fields = [
            'full_name',
            'gender',
            'date_of_birth',
            'location',
            'alternate_mobile',
            'hint_name',
        ]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user is not None:
            self.fields['email'].initial = user.email

    def save(self, user, commit=True):
        profile = super().save(commit=False)
        # Update user's email if provided
        new_email = self.cleaned_data.get('email')
        if new_email is not None:
            user.email = new_email
            if commit:
                user.save(update_fields=['email'])
        if commit:
            profile.save()
        return profile






