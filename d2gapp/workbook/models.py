from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

OFFICE = (
    ('d', 'Deacon'),
    ('t', 'Teacher'),
    ('p', 'Priest'),
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
    user = models.ForeignKey(User)
    office = models.CharField(max_length = 2, choices = OFFICE)

    def __unicode__(self):
        return self.user.username

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
    
    
