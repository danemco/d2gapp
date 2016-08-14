from django import forms
from .models import Assignment, PersonProgress, OFFICE, ProfileNotify

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = PersonProgress
        fields = ['profile', 'assignment', 'act1', 'act2', 'act3', 'share']
        widgets = {
                'profile': forms.HiddenInput(),
                'assignment': forms.HiddenInput(),
                }

    def __init__(self, assignment, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        if not assignment.act2:
            self.fields['act2'].widget = forms.HiddenInput()
        
        if not assignment.act3:
            self.fields['act3'].widget = forms.HiddenInput()
        
        if not assignment.share_has_textarea:
            self.fields['share'].widget = forms.HiddenInput()

class ReviewSectionForm(forms.Form):
    my_signature = forms.CharField(max_length=45)
    review_by = forms.ChoiceField(choices=())

    def __init__(self, profile, personprogress, *args, **kwargs):
        super(ReviewSectionForm, self).__init__(*args, **kwargs)
        self.fields['review_by'] = forms.ChoiceField(
            choices = [(p.id, p.name) for p in ProfileNotify.objects.filter(profile=profile)]
        )
        self.fields['personprogress'] = personprogress

class ProfileLoginForm(forms.Form):
    phone = forms.CharField(help_text="Use your 10 digit phone number without dashes or parenthesis.", max_length=10)
    last_name = forms.CharField()

class ProfileNotifyForm(forms.ModelForm):
    class Meta:
        model = ProfileNotify
        fields = ['phone', 'name']
        widgets = {
                'phone': forms.TextInput(attrs={"placeholder": "Phone Number", 'class': 'form-control'}),
                'name': forms.TextInput(attrs={"placeholder": "Name", 'class': 'form-control'}),
                }
