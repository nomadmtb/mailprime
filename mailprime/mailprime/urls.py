from django.conf.urls import patterns, include, url
from mailer import views

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mailprime.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', include('mailer.urls')),
    url(r'^$', views.index, name='index'),
	url(r'^login$', views.login, name='login'),
	url(r'^logout$', views.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
