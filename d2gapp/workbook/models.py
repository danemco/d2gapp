from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

OFFICE = (
    ('d', 'Deacon'),
    ('t', 'Teacher'),
    ('p', 'Priest'),
    ('-', 'Leader, Bishop, Advisor'),
)

SECTION = (
    ('ss', 'Spiritual Strength'),
    ('pd', 'Priesthood Duties'),
    ('ftsoy', 'For The Strenght Of Youth'),
    ('mp', 'Preparing To Receive the Melchizedek Priesthood'),
)

# Create your models here.
class Assignment(models.Model):
    office = models.CharField(max_length = 2, choices = OFFICE, default='d')
    section = models.CharField(max_length = 5, choices = SECTION, default='ss')
    title = models.CharField(max_length = 200)
    learn = models.TextField()
    act1 = models.TextField()
    act2 = models.TextField(blank = True, null = True)
    share = models.TextField()
    share_has_textarea = models.BooleanField(default = False)

    def __unicode__(self):
        return self.title

class Profile(models.Model):
    user = models.OneToOneField(User)
    office = models.CharField(max_length = 2, choices = OFFICE)
    phone = models.CharField(max_length = 10, "phone number", help_text="Phone number for receiving text messages and for connecting you with others", blank = True, null = True)
    ward = models.CharField(max_length = 50, "ward or branch", blank = True, null = True)

    def __unicode__(self):
        return self.user.username

class ProfileNotify(models.Model):
    """
    This model collects the names and phone numbers of those that the young man wishes to 
    notify when an assignment is completed.
    """
    profile = models.ForeignKey(Profile)
    phone = models.CharField(max_length = 10)
    name = models.CharField(max_length = 50)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.profile, self.name, self.phone)

class PersonProgress(models.Model):
    profile = models.ForeignKey(Profile)
    assignment = models.ForeignKey(Assignment)
    act1 = models.TextField()
    act2 = models.TextField(blank = True, null = True)
    share = models.TextField(blank = True, null = True)
    date_completed = models.DateTimeField(auto_now_add = True)
    shared_with = models.CharField(max_length=30, blank = True, null = True)

    def __unicode__(self):
        return "%s - %s" % (self.profile, self.assignment)

    class Meta:
        verbose_name_plural = 'person progress records'
    
    
