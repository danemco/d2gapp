from django import forms
from .models import Assignment, PersonProgress, OFFICE, ProfileNotify

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = PersonProgress
        fields = ['profile', 'assignment', 'act1', 'act2', 'share']
        widgets = {
                'profile': forms.HiddenInput(),
                'assignment': forms.HiddenInput(),
                }

    def __init__(self, assignment, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        if not assignment.act2:
            self.fields['act2'].widget = forms.HiddenInput()
        
        if not assignment.share_has_textarea:
            self.fields['share'].widget = forms.HiddenInput()

class ProfileLoginForm(forms.Form):
    phone = forms.CharField()
    last_name = forms.CharField()

class ProfileNotifyForm(forms.ModelForm):
    class Meta:
        model = ProfileNotify
        fields = ['phone', 'name']
        widgets = {
                'phone': forms.TextInput(attrs={"placeholder": "Phone Number", 'class': 'form-control'}),
                'name': forms.TextInput(attrs={"placeholder": "Name", 'class': 'form-control'}),
                }
