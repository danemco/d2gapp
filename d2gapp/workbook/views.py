from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.http.response import HttpResponseRedirect

from .models import Assignment, PersonProgress, Profile, ProfileNotify
from .forms import AssignmentForm, ProfileLoginForm

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

class RegisterProfileView(CreateView):
    success_url = reverse_lazy('assignment_list')
    model = Profile
    fields = ['first_name', 'last_name', 'office', 'phone', 'receive_text_messages', 'ward']

    def form_valid(self, form):
        retval = super(RegisterProfileView, self).form_valid(form)

        self.request.session['profile_id'] = self.object
        messages.add_message(self.request, messages.SUCCESS, "Profile successfully created!")

        return retval

class UpdateProfileView(UpdateView):
    success_url = reverse_lazy('profile_detail')
    model = Profile
    fields = ['first_name', 'last_name', 'office', 'phone', 'receive_text_messages', 'ward']

    def get_object(self, queryset=None):
        try:
            p = Profile.objects.get(pk=self.request.session.get('profile_id'))
        except ObjectDoesNotExist:
            raise Http404("No profile found. Try logging in or creating one.") 
        return p

class ProfileDetailView(TemplateView):
    template_name = 'workbook/profile_detail.html'
    
    def get_context_data(self):
        context = super(ProfileDetailView, self).get_context_data()
        pid = self.request.session.get('profile_id')
        try:
            context['profile'] = Profile.objects.get(pk=pid)
        except ObjectDoesNotExist:
            raise Http404("No profile found. Try logging in or creating one.") 

        return context

class ProfileLoginView(FormView):
    template_name = 'workbook/profile_login.html'
    form_class = ProfileLoginForm

    def get_success_url(self):
        return self.request.GET.get('next', '/')

    def form_valid(self, form):
        phone = form.cleaned_data['phone']
        last_name = form.cleaned_data['last_name']

        try:
            p = Profile.objects.get(phone=phone)
        except ObjectDoesNotExist:
            messages.add_message(self.request, messages.ERROR, "Invalid login. Try again.")
            return HttpResponseRedirect(reverse('profile_login'))

        self.request.session['profile_id'] = p.id

        messages.add_message(self.request, messages.SUCCESS, "Login successful. Welcome back!")
        return super(ProfileLoginView, self).form_valid(form)

class ProfileLogoutView(TemplateView):
    template_name = 'workbook/profile_logout.html'

    def get(self, request, *args, **kwargs):
        try:
            del request.session['profile_id']
        except KeyError:
            pass

        return super(ProfileLogoutView, self).get(request, *args, **kwargs)
