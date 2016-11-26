from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

OFFICE = (
    ('d', 'Deacon'),
    ('t', 'Teacher'),
    ('z', 'Priest'),
    ('-', 'Advisor, Bishop, or Parent'),
)

SECTION = (
    ('ss', 'Spiritual Strength'),
    ('pd', 'Priesthood Duties'),
    ('ftsoy', 'For The Strength Of Youth'),
    ('mp', 'Preparing To Receive the Melchizedek Priesthood'),
)

# Create your models here.
class Assignment(models.Model):
    office = models.CharField(max_length = 2, choices = OFFICE, default='d', verbose_name="priesthood office")
    section = models.CharField(max_length = 5, choices = SECTION, default='ss')
    title = models.CharField(max_length = 200)
    learn = models.TextField()
    act1 = models.TextField()
    act2 = models.TextField(blank = True, null = True)
    act3 = models.TextField(blank = True, null = True)
    share = models.TextField()
    share_has_textarea = models.BooleanField(default = False)
    review = models.BooleanField(default = False, verbose_name="is this assignment a review item")
    footnote = models.TextField(blank = True, null = True)
    ordering = models.IntegerField(blank = True, null = True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['office', 'ordering']
class Stake(models.Model):
    name = models.CharField(max_length = 50)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return self.name

class Unit(models.Model):
    stake = models.ForeignKey(Stake, blank=True, null=True)
    ward = models.CharField("ward or branch", max_length = 50, blank = True, null = True)
    password = models.CharField(max_length = 50, null=True, blank=True)
    active = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s" % (self.ward,)

    class Meta:
        ordering = ['stake', 'ward']

class DefaultNotifier(models.Model):
    SHOW_TO_OFFICES = (
        ('d', 'Deacons Only'),
        ('t', 'Teachers Only'),
        ('z', 'Priests Only'),
        ('-', 'All Young Men'),
    )

    unit = models.ForeignKey(Unit)
    phone = models.CharField(max_length = 10)
    position = models.CharField(max_length = 30)
    name = models.CharField(max_length = 50)
    show_to = models.CharField(max_length = 2, choices = SHOW_TO_OFFICES, default='-')

    def __unicode__(self):
        return "%s (%s - %s)" % (self.name, self.unit.stake, self.unit.ward)
    

class Profile(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    office = models.CharField(max_length = 2, choices = OFFICE, verbose_name="priesthood office")
    phone = models.CharField("phone number", max_length = 10, help_text="Use your full 10 digit phone number for receiving text messages", blank = True, null =  True)
    receive_text_messages = models.BooleanField(default=True)
    # Note: ward isn't in use anymore, but here for old Profile records that had an assigned ward
    ward = models.CharField("ward or branch", max_length = 50, blank = True, null = True)
    unit = models.ForeignKey(Unit)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

class ProfileNotify(models.Model):
    """
    This model collects the names and phone numbers of those that the young man wishes to 
    notify when an assignment is completed.
    """
    profile = models.ForeignKey(Profile)
    phone = models.CharField(max_length = 10)
    name = models.CharField(max_length = 50)
    position = models.CharField(max_length = 30, blank = True, null = True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.profile, self.name, self.phone)

    class Meta:
        verbose_name_plural = 'profile notifications'
        verbose_name = 'profile notification'

class PersonProgress(models.Model):
    profile = models.ForeignKey(Profile)
    assignment = models.ForeignKey(Assignment)
    act1 = models.TextField()
    act2 = models.TextField(blank = True, null = True)
    act3 = models.TextField(blank = True, null = True)
    share = models.TextField(blank = True, null = True)
    date_completed = models.DateTimeField(auto_now_add = True)
    shared_with = models.CharField(max_length=80, blank=True, null=True)
    review_requested_to = models.ForeignKey('ProfileNotify', blank=True, null=True)
    reviewed_by = models.ForeignKey(Profile, blank=True, null=True, related_name='reviewed_list')
    review_completed = models.DateTimeField(blank = True, null = True)

    def __unicode__(self):
        return "%s - %s" % (self.profile, self.assignment)

    class Meta:
        verbose_name_plural = 'person progress records'
        unique_together = ('profile', 'assignment')
        ordering = ['date_completed']
    
    
class StakeAdmin(models.Model):
    user = models.OneToOneField(User)
    stake = models.ForeignKey(Stake)

    def __unicode__(self):
        return "%s - %s" % (self.user, self.stake)


