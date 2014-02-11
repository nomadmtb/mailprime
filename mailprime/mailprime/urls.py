from django.conf.urls import patterns, include, url
from mailer import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mailprime.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', include('mailer.urls')),
    url(r'^$', views.index, name='index'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
	url(r'^home$', views.home, name='home'),
	url(r'^home/(\d)$', views.campaign, name='campaign'),
    url(r'^(\w+)/account$', views.user_account, name='user_account'),
    url(r'^(\w+)/campaigns$', views.user_campaigns, name='user_campaigns'),
    url(r'^(\w+)/(\d+)$', views.user_campaign, name='user_campaign'),
    url(r'^(\w+)/(\d+)/recipients$', views.user_campaign_recipients, name='user_campaign_recipients'),
)

# For Development ONLY. Remove when in production...
urlpatterns += staticfiles_urlpatterns()