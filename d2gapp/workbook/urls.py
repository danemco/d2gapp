from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns, include
from . import views
from .decorators import profile_required

urlpatterns = [
        # Assignment-related views
        url(r'^$', profile_required(views.AssignmentListView.as_view()), name="assignment_list"),
        url(r'^assignment/(?P<assignment>\d+)/create/$', profile_required(views.CompleteAssignmentView.as_view()), name="assignment_create"),

        # Profile-reltaed views
        url(r'profile/create/$', profile_required(views.RegisterProfileView.as_view()), name="profile_create"),
        url(r'profile/update/$', profile_required(views.UpdateProfileView.as_view()), name="profile_update"),
        url(r'profile/login/$', views.ProfileLoginView.as_view(), name='profile_login'),
        url(r'profile/logout/$', views.ProfileLogoutView.as_view(), name='profile_logout'),
        url(r'profile/$', profile_required(views.ProfileDetailView.as_view()), name="profile_detail"),

]
