from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns, include
from . import views

urlpatterns = [
        url(r'^$', views.AssignmentListView.as_view(), name="assignment_list"),
        # url(r'^assignment/(?P<pk>\d+)/$', views.AssignmentDetailView.as_view(), name="assignment_detail"),
        url(r'^assignment/(?P<assignment>\d+)/create/$', views.CompleteAssignmentView.as_view(), name="assignment_create"),

]
