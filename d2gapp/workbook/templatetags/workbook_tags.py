from django import template
from workbook.models import PersonProgress, Profile, Assignment

register = template.Library()

"""
Returns the personprogress object id given an assignment and a profile.
"""
@register.filter
def get_pp(assignment, profile):
    return PersonProgress.objects.get(profile = profile, assignment = assignment)

@register.filter
def office(qs, office):
    return qs.filter(office = office)

@register.simple_tag
def assignments_completed(profile):
    assignments = []
    for pp in PersonProgress.objects.filter(profile = profile):
        if pp.shared_with is not None:
            if pp.assignment.review:
                if pp.reviewed_by is not None:
                    assignments.append(pp.assignment)
            else:
                assignments.append(pp.assignment)

    return assignments

