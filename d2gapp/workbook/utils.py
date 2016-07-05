from .models import Assignment, PersonProgress, Profile, ProfileNotify
from django.conf import settings
from twilio.rest import TwilioRestClient
import os

"""
Notify the people on the peson's profile that this individual completed his assignments.
"""
def notify_completed_assignment(profile, assignment):
    client = TwilioRestClient(os.environ['TWILIO_ACCOUNT_SID'], os.environ['TWILIO_AUTH_TOKEN'])

    for pn in profile.profilenotify_set.all():
        print "Notifying %s at phone number %s" % (pn.name, pn.phone)
        m = client.messages.create(to='+1' + pn.phone, 
                from_='+1' + getattr(settings, "DEFAULT_FROM_SMS", None),
                body="D2G APP: %s completed the activity, %s" % (profile, assignment))
