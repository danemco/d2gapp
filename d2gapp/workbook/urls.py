from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns, include
from . import views
from .decorators import profile_required

urlpatterns = [
        # Assignment-related views
        url(r'^profile-activity/$', profile_required(views.AssignmentListView.as_view()), name="assignment_list"),
        url(r'^activity/(?P<assignment>\d+)/complete/$', profile_required(views.CompleteAssignmentView.as_view()), name="assignment_create"),
        url(r'^activity/(?P<assignment>\d+)/update/$', profile_required(views.UpdateAssignmentView.as_view()), name="assignment_update"),

        # Profile-reltaed views
        url(r'^profile/create/$', views.RegisterProfileView.as_view(), name="profile_create"),
        url(r'^profile/update/$', profile_required(views.UpdateProfileView.as_view()), name="profile_update"),
        url(r'^profile/login/$', views.ProfileLoginView.as_view(), name='profile_login'),
        url(r'^profile/logout/$', views.ProfileLogoutView.as_view(), name='profile_logout'),
        url(r'^profile/$', profile_required(views.ProfileDetailView.as_view()), name="profile_detail"),
        url(r'^profile/notify/add/$', profile_required(views.ProfileNotifyAdd.as_view()), name="profile_notify_add"),
        url(r'^profile/notify/delete/(?P<pk>\d+)/$', profile_required(views.ProfileNotifyDelete.as_view()), name="profile_notify_delete"),

        # Leader-specific views
        url(r'^leader-report/$', profile_required(views.LeaderReportView.as_view()),name="leader_report"),

]
