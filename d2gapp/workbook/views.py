from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import CreateView, FormView
from django.core.urlresolvers import reverse_lazy

from .models import Assignment, PersonProgress, Profile, ProfileNotify
from .forms import AssignmentForm, RegistrationForm
from django.contrib.auth.models import User

import random

RANDOM_ALPHABET = 'abcdfghjklmnpqrstuvwxyzABCDFGHJKLMNPQRSTVWXYZ1234567890'

# Create your views here.
class AssignmentListView(ListView):
    model = Assignment

class AssignmentDetailView(DetailView):
    model = Assignment

class CompleteAssignmentView(CreateView):
    model = PersonProgress
    form_class = AssignmentForm
    success_url = reverse_lazy('assignment_list')
    
    def get_form_kwargs(self):
        kwargs = super(CompleteAssignmentView, self).get_form_kwargs()
        kwargs['assignment'] = get_object_or_404(Assignment, pk = self.kwargs.get('assignment', None))
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CompleteAssignmentView, self).get_context_data(**kwargs)
        context['assignment'] = get_object_or_404(Assignment, pk = self.kwargs.get('assignment', None))
        return context

    def get_initial(self):
        init_data = {}
        init_data['profile'] = get_object_or_404(Profile, user = self.request.user)
        init_data['assignment'] = get_object_or_404(Assignment, pk = self.kwargs.get('assignment', None))
        return init_data

class RegisterView(FormView):
    form_class = RegistrationForm
    success_url = '/thanks/' # TODO edit this
    template_name = 'workbook/register_user.html'

    def form_valid(self, form):
        try:
            # got the rand_strong concept from stackoverflow.com/questions/2257441
            rand_string = ''.join(random.choice(RANDOM_ALPHABET) for _ in range(6))
            u = User()
            p = Profile() 
            u.first_name = form.cleaned_data['first_name']
            u.last_login = form.cleaned_data['last_name']
            # username is first name plus last name plus random string
            u.username = form.cleaned_data['first_name'].replace(' ', '_') \
                         + form.cleaned_data['last_name'].replace(' ', '_') \
                         + rand_string
            u.save()
            p.user = u
            p.office = form.cleaned_data['office']
            p.phone = form.cleaned_data['phone']
            p.ward = form.cleaned_data['ward']
            p.save()

        except:
            pass
        return super(RegisterView, self).form_valid(form)
