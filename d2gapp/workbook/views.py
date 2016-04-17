from django.shortcuts import render, get_object_or_404
from django.views.generic import DetailView, TemplateView, ListView
from django.views.generic.edit import CreateView
from django.core.urlresolvers import reverse_lazy

from .models import Assignment, PersonProgress, Profile
from .forms import AssignmentForm

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



