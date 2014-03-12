from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from django.http import Http404
from mailer.forms import CampaignForm, MessageForm, LoginForm

# The user-campaign-message-events-view will show all of the events associated with a particular message
def user_campaign_message_events(request, param_username, param_campaign_pk, param_message_pk):
	page_vars = {"page_title": 'Message Events'}

	if current_user(request) and request.user.username == param_username:
		events = Event.objects.filter(message__campaign__pk = param_campaign_pk, message__pk = param_message_pk)
		page_vars['events'] = events
		return render(request, 'event/user_campaign_message_events.html', page_vars)
	else:
		raise Http404

def user_campaign_message_event(request, param_username, param_campaign_pk, param_message_pk, param_event_pk):
	page_vars = {"page_title": 'View Event'}

	if current_user(request) and request.user.username == param_username:
		try:
			event = Event.objects.get(pk = param_event_pk, recipient__campaign__pk = param_campaign_pk, message__pk = param_message_pk)
		except Event.DoesNotExist:
			messages.add_message(request, messages.WARNING, "Something went wrong")
			raise Http404

		page_vars['event'] = event
		return render(request, 'event/user_campaign_message_event.html', page_vars)
	else:
		raise Http404