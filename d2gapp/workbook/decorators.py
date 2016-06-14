from .models import Assignment, PersonProgress, Profile, ProfileNotify
from django.http import HttpResponseRedirect


def profile_required(function):
    # Not quite sure what I'm doing
    def decorator(request, *args, **kwargs):
        # If we have a profile ID set in the profile, just return the function
        if request.session.get('profile_id', None):
            return function(request, *args, **kwargs)
        # Otherwise, redirect to a view that gets the profile
        path = request.get_full_path()
        return HttpResponseRedirect(redirect_to = '/profile/login/?next=' + path)
    return decorator
