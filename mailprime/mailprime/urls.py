from django.conf.urls import patterns, include, url
from mailer import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.index, name='index'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
    url(r'^(\w+)/account$', views.user_account, name='user_account'),
    url(r'^(\w+)/campaigns$', views.user_campaigns, name='user_campaigns'),
    url(r'^(\w+)/campaign-(\d+)$', views.user_campaign, name='user_campaign'),
    url(r'^(\w+)/campaign-(\d+)/stats$', views.campaign_statistics, name='campaign_statistics'),
    url(r'^(\w+)/campaign-(\d+)/recipients$', views.user_campaign_recipients, name='user_campaign_recipients'),
    url(r'^(\w+)/campaign-(\d+)/messages$', views.user_campaign_messages, name='user_campaign_messages'),
    url(r'^(\w+)/campaign-(\d+)/message-(\d+)$', views.user_campaign_message, name='user_campaign_message'),
    url(r'^(\w+)/campaign-(\d+)/message-(\d+)/stats$', views.message_statistics, name='message_statistics'),
    url(r'^(\w+)/campaign-(\d+)/message-(\d+)/events$', views.user_campaign_message_events, name='user_campaign_message_events'),
    url(r'^(\w+)/campaign-(\d+)/message-(\d+)/event-(\d+)$', views.user_campaign_message_event, name='user_campaign_message_event'),
    url(r'^tracker/visit/(\w+)/(\w+)\.jpg$', views.tracker_visit, name='tracker_visit'),
    url(r'^tracker/unsubscribe/(\w+)$', views.tracker_unsubscribe, name='tracker_unsubscribe'),
)

# For Development ONLY. Remove when in production...
urlpatterns += staticfiles_urlpatterns()