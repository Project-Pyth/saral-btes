from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from myapp.models import UserProfile, Notification, Personalnote, LeaveApply


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (

            'first_name',
            'last_name',
        )

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            return ValidationError('first name must contain only letters')
        return first_name



class PersonalEditForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('designation',
                  'contact',
                  'address',
                  'image',
                  )


class NotificationForm(forms.ModelForm):
    Subject = forms.CharField(widget=forms.TextInput(attrs={'size': 36}))

    class Meta:
        model = Notification
        fields = ('To',
                  'Subject',
                  'Content',
                  )


class PersonalForm(forms.ModelForm):
    class Meta:
        model = Personalnote
        fields = ('Content',
                  'Sub',
                  )


class LeaveApplyForm(forms.ModelForm):
    class Meta:
        model = LeaveApply
        widgets = {'date': forms.DateInput(attrs={'class': 'datepicker'})}
        fields = (
            'days_asked',
            'date',
            'reason',
        )
