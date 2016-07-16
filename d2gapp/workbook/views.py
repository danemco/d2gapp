from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect

from .models import Assignment, PersonProgress, Profile, ProfileNotify
from .forms import AssignmentForm, ProfileLoginForm, ProfileNotifyForm
from .utils import notify_completed_assignment

# Create your views here.
class AjaxableResponseMixin(object):
    """
    Mixin to add AJAX support to a form.
    Must be used with an object-based FormView (e.g. CreateView)
    """
    def form_invalid(self, form):
        response = super(AjaxableResponseMixin, self).form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        else:
            return response

    def form_valid(self, form):
        # We make sure to call the parent's form_valid() method because
        # it might do some processing (in the case of CreateView, it will
        # call form.save() for example).
        response = super(AjaxableResponseMixin, self).form_valid(form)
        if self.request.is_ajax():
            data = model_to_dict(self.object)
            return JsonResponse(data)
        else:
            return response

class AssignmentListView(ListView):
    model = Assignment

    def get_queryset(self):
        """
        Show only assignments for the specific office.
        """
        queryset = super(AssignmentListView, self).get_queryset()
        p = self.request.session.get('profile')
        
        if (p.office != '-'):
            return queryset.filter(office = p.office)
        else:
            return queryset

    def get_context_data(self, **kwargs):
        """
        Add the list of completed assignments to the list
        """
        context = super(AssignmentListView, self).get_context_data(**kwargs)

        p = self.request.session.get('profile')
        profile_assignment_completed = []

        for pp in p.personprogress_set.all():
            profile_assignment_completed.append(pp.assignment)

        context['profile_assignment_completed'] = profile_assignment_completed

        return context

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
        init_data['profile'] = self.request.session['profile']
        init_data['assignment'] = get_object_or_404(Assignment, pk = self.kwargs.get('assignment', None))
        return init_data

    def form_valid(self, form):
        retval = super(CompleteAssignmentView, self).form_valid(form)

        profile = self.request.session['profile']
        notify_completed_assignment(profile, self.object)
        messages.add_message(self.request, messages.SUCCESS, "Activity Complete: %s" % self.object.assignment)

        return retval

class UpdateAssignmentView(UpdateView):
    model = PersonProgress
    form_class = AssignmentForm
    success_url = reverse_lazy('assignment_list')

    def get_object(self):
        assignment = self.kwargs.get('assignment', None)
        profile    = self.request.session['profile']

        obj = get_object_or_404(PersonProgress, assignment = assignment, profile = profile)

        return obj

    def get_form_kwargs(self):
        kwargs = super(UpdateAssignmentView, self).get_form_kwargs()
        kwargs['assignment'] = get_object_or_404(Assignment, pk = self.kwargs.get('assignment', None))
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(UpdateAssignmentView, self).get_context_data(**kwargs)
        context['assignment'] = get_object_or_404(Assignment, pk = self.kwargs.get('assignment', None))
        return context

    def form_valid(self, form):
        """
        Set the message saying that the activity has been updated.
        """
        retval = super(UpdateAssignmentView, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Activity Updated: %s" % self.object.assignment)
        return retval

    
class RegisterProfileView(CreateView):
    success_url = reverse_lazy('assignment_list')
    model = Profile
    fields = ['first_name', 'last_name', 'office', 'phone', 'receive_text_messages', 'ward']

    def form_valid(self, form):
        retval = super(RegisterProfileView, self).form_valid(form)

        self.request.session['profile'] = self.object
        messages.add_message(self.request, messages.SUCCESS, "Profile successfully created!")

        return retval

class UpdateProfileView(UpdateView):
    success_url = reverse_lazy('profile_detail')
    model = Profile
    fields = ['first_name', 'last_name', 'office', 'phone', 'receive_text_messages', 'ward']

    def get_object(self, queryset=None):
        try:
            p = self.request.session.get('profile')
        except ObjectDoesNotExist:
            raise Http404("No profile found. Try logging in or creating one.") 
        return p

    def get_context_data(self):
        context = super(UpdateProfileView, self).get_context_data()
        context['form2'] = ProfileNotifyForm
        return context

class ProfileDetailView(TemplateView):
    template_name = 'workbook/profile_detail.html'
    
    def get_context_data(self):
        context = super(ProfileDetailView, self).get_context_data()
        context['profile'] = self.request.session.get('profile')

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

        self.request.session['profile'] = p

        messages.add_message(self.request, messages.SUCCESS, "Login successful. Welcome back!")
        return super(ProfileLoginView, self).form_valid(form)

class ProfileLogoutView(TemplateView):
    template_name = 'workbook/profile_logout.html'

    def get(self, request, *args, **kwargs):
        try:
            del request.session['profile']
        except KeyError:
            pass

        return super(ProfileLogoutView, self).get(request, *args, **kwargs)

class ProfileNotifyAdd(AjaxableResponseMixin, CreateView):
    model = ProfileNotify
    fields = ['phone', 'name']
    success_url = reverse_lazy('profile_detail')

    def form_valid(self, form):
        try:
            p = self.request.session.get('profile')
        except ObjectDoesNotExist:
            raise Http404("No profile found. Try logging in or creating one.") 
        form.instance.profile = p
        if not self.request.is_ajax:
            messages.add_message(self.request, messages.SUCCESS, "%s successfully added to notification list." % form.instance.name)
        return super(ProfileNotifyAdd, self).form_valid(form)

class ProfileNotifyDelete(AjaxableResponseMixin, DeleteView):
    model = ProfileNotify
    success_url = reverse_lazy('profile_detail')

class LeaderReportView(TemplateView):
    template_name = "workbook/leader_view.html"

    def get_context_data(self, **kwargs):
        """
        Get a list of people that report to this person
        """
        context = super(LeaderReportView, self).get_context_data(**kwargs)

        context["assignment_list"] = Assignment.objects.all()

        # Get a list of profiles that report to the logged in user
        try:
            user_profile = self.request.session.get('profile')
        except ObjectDoesNotExist:
            raise Http404("No profile found. Try logging in or creating one.") 


        reporting_profiles = []
        for pn in ProfileNotify.objects.filter(phone = user_profile.phone):
            reporting_profiles.append(pn.profile)

        # Sort by last name
        reporting_profiles.sort(key=lambda x: (x.office, x.last_name))

        context["reporting_profile_list"] = reporting_profiles

        return context



