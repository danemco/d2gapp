from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns, include
from . import views

urlpatterns = [
        url(r'^$', views.AssignmentListView.as_view(), name="assignment_list"),

]