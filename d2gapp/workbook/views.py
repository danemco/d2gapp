from django.shortcuts import render
from django.views.generic import DetailView, TemplateView, ListView

from .models import Assignment, PersonProgress

# Create your views here.
class AssignmentListView(ListView):
    model = Assignment
