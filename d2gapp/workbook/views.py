from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView, View
from django.views.generic.edit import CreateView, FormView, UpdateView, DeleteView
from django.core import serializers
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404, JsonResponse
from django.contrib import messages
from django.forms.models import model_to_dict
from django.http.response import HttpResponseRedirect
from django.utils import timezone

from django.contrib.auth.models import User

from .models import Assignment, PersonProgress, Profile, ProfileNotify, Unit, DefaultNotifier, StakeAdmin
from .forms import AssignmentForm, ProfileLoginForm, ProfileNotifyForm, ReviewSectionForm, PrepareTextMessageForm, RegisterProfileForm
from .utils import notify_completed_assignment, notify_review_assignment

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
        profile_assignment_started   = []

        for pp in p.personprogress_set.all():
            if pp.shared_with != "" and pp.shared_with is not None:
                profile_assignment_completed.append(pp.assignment)
            else:
                profile_assignment_started.append(pp.assignment)

        context['profile_assignment_completed'] = profile_assignment_completed
        context['profile_assignment_started']   = profile_assignment_started

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

class CompleteReviewAssignmentView(FormView):
    form_class = ReviewSectionForm
    template_name = 'workbook/review_assignment.html'

    success_url = reverse_lazy('assignment_list')

    def get_form_kwargs(self):
        kwargs = super(CompleteReviewAssignmentView, self).get_form_kwargs()
        kwargs['profile'] = self.request.session['profile']
        # kwargs['personprogress'] = self.request.session['profile'] # commented out because I don't think I need it
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(CompleteReviewAssignmentView, self).get_context_data(**kwargs)
        context['assignment'] = get_object_or_404(Assignment, pk = self.kwargs.get('assignment', None))
        return context

    def form_valid(self, form):
        retval = super(CompleteReviewAssignmentView, self).form_valid(form)
        pn = ProfileNotify.objects.get(pk = form.cleaned_data['review_by'])

        pp = PersonProgress()
        pp.profile = self.request.session['profile']
        pp.assignment = get_object_or_404(Assignment, pk = self.kwargs.get('assignment', None))
        pp.act1 = form.cleaned_data['my_signature']
        pp.review_requested_to = pn
        pp.shared_with = str(pn)
        self.object = pp.save()

        notify_review_assignment(pn, pp)
        messages.add_message(self.request, messages.SUCCESS, "Request for seview sent to %s" % pn.name)

        return retval

class SignReviewForm(AjaxableResponseMixin, UpdateView):
    model = PersonProgress
    fields = ['reviewed_by']
    success_url = reverse_lazy('leader_report')

    def form_valid(self, form):
        retval = super(SignReviewForm, self).form_valid(form)
        pp = self.object

        pp.reviewed_by = self.request.session.get('profile')
        pp.review_completed = timezone.now()

        pp.save()
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
    success_url = reverse_lazy('profile_update')
    form_class = RegisterProfileForm
    template_name = 'workbook/profile_form.html'

    def form_valid(self, form):
        retval = super(RegisterProfileView, self).form_valid(form)

        self.request.session['profile'] = self.object
        messages.add_message(self.request, messages.SUCCESS, "Profile successfully created!")
        messages.add_message(self.request, messages.ERROR, '<i class="material-icons">priority_high</i> NEXT STEP: Add key people (such as a parent) to receive a text message when you complete an activity by editing the information below.')

        # Prepopulate default notifications for the given unit
        for dn in self.object.unit.defaultnotifier_set.all():
            if dn.show_to == '-' or dn.show_to == self.object.office:
                pn = ProfileNotify()
                pn.profile = self.object
                pn.phone   = dn.phone
                pn.position = dn.position
                pn.name    = dn.name
                pn.save()

        return retval

    def get_context_data(self):
        context = super(RegisterProfileView, self).get_context_data()
        context['unit_list'] = Unit.objects.all()
        return context

class UpdateProfileView(UpdateView):
    success_url = reverse_lazy('profile_detail')
    model = Profile
    form_class = RegisterProfileForm

    def get_object(self, queryset=None):
        try:
            p = self.request.session.get('profile')
        except ObjectDoesNotExist:
            raise Http404("No profile found. Try logging in or creating one.") 
        return p

    def get_context_data(self, **kwargs):
        context = super(UpdateProfileView, self).get_context_data(**kwargs)
        context['form2'] = ProfileNotifyForm
        return context

    def form_valid(self, form):
        retval = super(UpdateProfileView, self).form_valid(form)

        self.request.session['profile'] = self.object
        messages.add_message(self.request, messages.SUCCESS, "Profile updated successfully!")

        return retval

    def get_initial(self):
        init_data = super(UpdateProfileView, self).get_initial()
        init_data['stake'] = self.object.unit.stake
        init_data['ward']  = self.object.unit
        return init_data

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
        return self.request.GET.get('next', reverse_lazy('assignment_list'))

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
        context["assignment_list_d"] = Assignment.objects.filter(office = 'd')
        context["assignment_list_t"] = Assignment.objects.filter(office = 't')
        context["assignment_list_p"] = Assignment.objects.filter(office = 'z')

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

class LeaderDetailView(DetailView):
    model = Profile
    template_name = 'workbook/leader_profile_detail.html'

    # Override get_object to ensure that the current logged in profile has permission to view this person's profile
    def get_object(self, queryset=None):
        obj = super(LeaderDetailView, self).get_object(queryset)

        try:
            user_profile = self.request.session.get('profile')
        except ObjectDoesNotExist:
            raise Http404("No profile found. Try logging in or creating one.") 


        reporting_profiles = []
        for pn in ProfileNotify.objects.filter(phone = user_profile.phone):
            reporting_profiles.append(pn.profile)

        if obj not in reporting_profiles:
            raise Http404("You don't have permission to view this person's profile information.")

        return obj

class PrepareTextMessageView(FormView):
    form_class = PrepareTextMessageForm
    success_url = reverse_lazy('leader_report')
    template_name = 'workbook/prepare_text_message.html'

    def get_form_kwargs(self):
        kwargs = super(PrepareTextMessageView, self).get_form_kwargs()
        kwargs['profile'] = self.request.session['profile']
        # kwargs['personprogress'] = self.request.session['profile'] # commented out because I don't think I need it
        return kwargs

    def form_valid(self, form):
        retval = super(PrepareTextMessageView, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Text message sent successfully.")

        return retval

class GetUnitsForStake(View):

    def get(self, request, *args, **kwargs):
        units = Unit.objects.all().filter(stake=self.kwargs.get('stake'), active=True)
        return JsonResponse({'unit_list': list(units.values('id', 'ward'))})

class StakeAdminWardList(ListView):
    model = Unit
    template_name = 'workbook/unit_list.html'

    def get_queryset(self):
        try:
            qs = super(StakeAdminWardList, self).get_queryset()
            qs = qs.filter(stake = self.request.user.stakeadmin.stake)
            return qs
        except User.stakeadmin.RelatedObjectDoesNotExist:
            return None

class StakeAdminWardUpdate(UpdateView):
    model = Unit
    fields = ['stake', 'ward', 'active']
    template_name = 'workbook/ward_form.html'
    success_url = reverse_lazy('ward_list')

    def get_context_data(self, **kwargs):
        context = super(StakeAdminWardUpdate, self).get_context_data(**kwargs)
        context['notification_list'] = DefaultNotifier.objects.filter(unit = self.kwargs.get('pk'))
        return context

    def form_valid(self, form):
        retval = super(StakeAdminWardUpdate, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Ward updated successfully.")
        return retval

class StakeAdminWardCreate(CreateView):
    model = Unit
    fields = ['stake', 'ward']
    template_name = 'workbook/ward_form.html'
    success_url = reverse_lazy('ward_list')

    def get_initial(self):
        initial_data = super(StakeAdminWardCreate, self).get_initial()
        initial_data['stake'] = self.request.user.stakeadmin.stake
        return initial_data

    def form_valid(self, form):
        retval = super(StakeAdminWardCreate, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Ward created successfully.")
        return retval

class StakeAdminDefaultNotifierUpdate(UpdateView):
    model = DefaultNotifier
    fields = ['name', 'position', 'phone', 'show_to']

    def get_success_url(self):
        return reverse('ward_update', kwargs={'pk': self.object.unit.id})

    def form_valid(self, form):
        retval = super(StakeAdminDefaultNotifierUpdate, self).form_valid(form)
        messages.add_message(self.request, messages.SUCCESS, "Details updated for " + self.object.name + ".")
        return retval

class StakeAdminDefaultNotifierCreate(CreateView):
    model = DefaultNotifier
    fields = ['name', 'position', 'phone', 'show_to']

    def get_success_url(self):
        return reverse('ward_update', kwargs={'pk': self.object.unit.id})

    def form_valid(self, form):
        form.instance.unit = Unit.objects.get(pk = self.kwargs.get('ward'))
        messages.add_message(self.request, messages.SUCCESS, "Successfully created default notification for " + form.instance.name + ".")
        return super(StakeAdminDefaultNotifierCreate, self).form_valid(form)


class StakeAdminDefaultNotifierDelete(DeleteView):
    model = DefaultNotifier
    
    def get_success_url(self):
        return reverse('ward_update', kwargs={'pk': self.kwargs.get('ward')})
