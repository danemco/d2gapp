from django import forms
from .models import Assignment, PersonProgress, OFFICE, ProfileNotify, Stake, Profile

class AssignmentForm(forms.ModelForm):

    class Meta:
        model = PersonProgress
        fields = ['profile', 'assignment', 'act1', 'act2', 'act3', 'share', 'shared_with']
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

    def __init__(self, profile, *args, **kwargs):
        super(ReviewSectionForm, self).__init__(*args, **kwargs)
        if ProfileNotify.objects.filter(profile=profile).count() > 0:
            self.fields['review_by'] = forms.ChoiceField(
                choices = [(p.id, p.name) for p in ProfileNotify.objects.filter(profile=profile)]
            )
        else:
            self.fields['review_by'] = forms.ChoiceField(
                choices = (('-', '-- Edit Profile To Add Advisor or Parent --'),)
            )
            
    class Meta:
        widgets = {
                'my_signature': forms.TextInput(attrs={'class': 'form-control'}),
                'review_by': forms.Select(attrs={'class': 'form-control'}),
                }

    def clean_review_by(self):
        data = self.cleaned_data['review_by']

        if data == '-':
            raise forms.ValidationError("You need to add a person to your notification list. Go to Edit My Profile to add a parent or advisor to your account.")

        return data

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

class PrepareTextMessageForm(forms.Form):
    message = forms.CharField(widget=forms.widgets.Textarea)
    send_to = forms.MultipleChoiceField(choices=(), widget=forms.CheckboxSelectMultiple(attrs={'checked': 'checked'}))

    def __init__(self, profile, *args, **kwargs):
        super(PrepareTextMessageForm, self).__init__(*args, **kwargs)
        reporting_profiles = []
        for pn in ProfileNotify.objects.filter(phone = profile.phone):
            reporting_profiles.append(pn.profile)

        self.fields['send_to'] = forms.MultipleChoiceField(
            choices = [(p.id, p.full_name()) for p in reporting_profiles],
            widget=forms.CheckboxSelectMultiple(attrs={'checked': 'checked'})
        )
class RegisterProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'office', 'phone', 'receive_text_messages', 'unit']

        widgets = {
                'unit': forms.Select(attrs={'class': 'form-control'}),
                }

    def __init__(self, *args, **kwargs):
        super(RegisterProfileForm, self).__init__(*args, **kwargs)
        self.fields['stake'] = forms.ModelChoiceField(
                Stake.objects.filter(active=True), 
                empty_label="Please Choose Your Stake",
                widget=forms.Select(attrs={'class': 'form-control'}))
