from django import forms
from .models import Assignment, PersonProgress

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = PersonProgress
        fields = ['act1', 'act2', 'share']

    def __init__(self, assignment, *args, **kwargs):
        super(AssignmentForm, self).__init__(*args, **kwargs)
        if not assignment.act2:
            self.fields['act2'].widget = forms.HiddenInput()
        
        if not assignment.share_has_textarea:
            self.fields['share'].widget = forms.HiddenInput()

