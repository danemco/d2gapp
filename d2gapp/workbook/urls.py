from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns, include
from . import views
from .decorators import profile_required

urlpatterns = [
        # Assignment-related views
        url(r'^profile-activity/$', profile_required(views.AssignmentListView.as_view()), name="assignment_list"),
        url(r'^activity/(?P<assignment>\d+)/complete/$', profile_required(views.CompleteAssignmentView.as_view()), name="assignment_create"),
        url(r'^activity/(?P<assignment>\d+)/update/$', profile_required(views.UpdateAssignmentView.as_view()), name="assignment_update"),
        url(r'^review-activity/(?P<assignment>\d+)/complete/$', profile_required(views.CompleteReviewAssignmentView.as_view()), name="review_create"),
        #url(r'^review-activity/(?P<assignment>\d+)/update/$', profile_required(views.UpdateReviewAssignmentView.as_view()), name="review_update"), # TODO
        url(r'^sign-activity/(?P<pk>\d+)/$', profile_required(views.SignReviewForm.as_view()), name="sign_personprogress"),

        # Profile-reltaed views
        url(r'^profile/create/$', views.RegisterProfileView.as_view(), name="profile_create"),
        url(r'^profile/update/$', profile_required(views.UpdateProfileView.as_view()), name="profile_update"),
        url(r'^profile/login/$', views.ProfileLoginView.as_view(), name='profile_login'),
        url(r'^profile/logout/$', views.ProfileLogoutView.as_view(), name='profile_logout'),
        url(r'^profile/$', profile_required(views.ProfileDetailView.as_view()), name="profile_detail"),
        url(r'^profile/notify/add/$', profile_required(views.ProfileNotifyAdd.as_view()), name="profile_notify_add"),
        url(r'^profile/notify/delete/(?P<pk>\d+)/$', profile_required(views.ProfileNotifyDelete.as_view()), name="profile_notify_delete"),
        url(r'^get-units-for-stake/(?P<stake>\d+)/$', views.GetUnitsForStake.as_view(), name="get-units-for-stake"),

        # Leader-specific views
        url(r'^leader-report/$', profile_required(views.LeaderReportView.as_view()),name="leader_report"),
        url(r'^leader-report/detail/(?P<pk>\d+)/$', profile_required(views.LeaderDetailView.as_view()),name="leader_detail"),
        url(r'^new-text-message/$', profile_required(views.PrepareTextMessageView.as_view()), name="send_text_message"),

        # Stake Admin views
        url(r'^stake-admin/$', login_required(views.StakeAdminWardList.as_view()), name='ward_list'),
#        url(r'^stake-admin/ward/(?P<pk>\d+)/$', login_required(views.StakeAdminWardDetail.as_view()), name='ward_detail'),
        url(r'^stake-admin/update/ward/(?P<pk>\d+)/$', login_required(views.StakeAdminWardUpdate.as_view()), name='ward_update'),
        url(r'^stake-admin/create/$', login_required(views.StakeAdminWardCreate.as_view()), name='ward_create'),
#         url(r'^stake-admin/delete/(?P<pk>\d+)/$', login_required(), name='ward_delete'),
#         url(r'^stake-admin/notify-list/ward/(?P<ward>\d+)/$', login_required(), name='defaultnotifier_list'),
        url(r'^stake-admin/notify-list/update/(?P<pk>\d+)/$', login_required(views.StakeAdminDefaultNotifierUpdate.as_view()), name='defaultnotifier_update'),
        url(r'^stake-admin/notify-list/create/ward/(?P<ward>\d+)/$', login_required(views.StakeAdminDefaultNotifierCreate.as_view()), name='defaultnotifier_create'),
        url(r'^stake-admin/notify-list/ward/(?P<ward>\d+)/delete/(?P<pk>\d+)/$', login_required(views.StakeAdminDefaultNotifierDelete.as_view()), name='defaultnotifier_delete'),

]
