from __future__ import unicode_literals

from django.db import models

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
    footnote = models.TextField(blank = True, null = True)
    ordering = models.IntegerField(blank = True, null = True)

    def __unicode__(self):
        return self.title

    class Meta:
        ordering = ['office', 'ordering']

class Profile(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    office = models.CharField(max_length = 2, choices = OFFICE, verbose_name="priesthood office")
    phone = models.CharField("phone number", max_length = 10, help_text="Use your full 10 digit phone number for receiving text messages", blank = True, null =  True)
    receive_text_messages = models.BooleanField(default=True)
    ward = models.CharField("ward or branch", max_length = 50, blank = True, null = True)

    def __unicode__(self):
        return "%s %s" % (self.first_name, self.last_name)

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
    shared_with = models.CharField(max_length=30, blank = True, null = True)

    def __unicode__(self):
        return "%s - %s" % (self.profile, self.assignment)

    class Meta:
        verbose_name_plural = 'person progress records'
        unique_together = ('profile', 'assignment')
    
    
