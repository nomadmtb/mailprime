from django.conf.urls import patterns, include, url
from mailer import campaign_views, tracker_views, general_views, recipient_views, message_views, event_views, json_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', general_views.index, name='index'),
	url(r'^login$', general_views.login, name='login'),
	url(r'^logout$', general_views.logout, name='logout'),
    url(r'^tos$', general_views.terms_of_service, name='terms_of_service'),
    url(r'^(\w+)/account$', general_views.user_account, name='user_account'),
    url(r'^(\w+)/campaigns$', campaign_views.user_campaigns, name='user_campaigns'),
    url(r'^(\w+)/campaigns/new$', campaign_views.user_campaign_new, name='user_campaign_new'),
    url(r'^(\w+)/campaign-(\d+)/edit$', campaign_views.user_campaign_edit, name='user_campaign_edit'),
    url(r'^(\w+)/campaign-(\d+)$', campaign_views.user_campaign, name='user_campaign'),
    url(r'^(\w+)/campaign-(\d+)/stats$', campaign_views.campaign_statistics, name='campaign_statistics'),
    url(r'^(\w+)/campaign-(\d+)/recipients$', recipient_views.user_campaign_recipients, name='user_campaign_recipients'),
    url(r'^(\w+)/campaign-(\d+)/recipients/upload$', recipient_views.upload_recipients, name='upload_recipients'),
    url(r'^(\w+)/campaign-(\d+)/recipients/add$', recipient_views.add_recipient, name='add_recipient'),
    url(r'^(\w+)/campaign-(\d+)/messages$', message_views.user_campaign_messages, name='user_campaign_messages'),
    url(r'^(\w+)/campaign-(\d+)/messages/new$', message_views.user_campaign_message_new, name='user_campaign_message_new'),
    url(r'^(\w+)/campaign-(\d+)/message-(\d+)$', message_views.user_campaign_message, name='user_campaign_message'),
    url(r'^(\w+)/campaign-(\d+)/message-(\d+)/stats$', message_views.message_statistics, name='message_statistics'),
    url(r'^(\w+)/campaign-(\d+)/message-(\d+)/events$', event_views.user_campaign_message_events, name='user_campaign_message_events'),
    url(r'^(\w+)/campaign-(\d+)/message-(\d+)/event-(\d+)$', event_views.user_campaign_message_event, name='user_campaign_message_event'),
    url(r'^tracker/visit/(\w+)/(\w+)\.jpg$', tracker_views.tracker_visit, name='tracker_visit'),
    url(r'^tracker/auth/(\w+)$', tracker_views.tracker_authorize, name='tracker_authorize'),
    url(r'^tracker/unsub/(\w+)$', tracker_views.tracker_unsubscribe, name='tracker_unsubscribe'),
    url(r'^api/(\w+)/c-(\d+)/m-(\d+)/region_data\.json$', json_views.get_message_region_data, name="get_message_region_data"),
    url(r'^api/(\w+)/c-(\d+)/m-(\d+)/sample_message\.html$', json_views.get_sample_message, name="get_sample_message"),
)

# For Development ONLY. Remove when in production...
urlpatterns += staticfiles_urlpatterns()