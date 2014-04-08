from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from django.http import Http404
from mailer.forms import CampaignForm, MessageForm, LoginForm

def tracker_visit(request, param_recipient_hash, param_message_hash):

	coordinates = geo_locate(request.META['REMOTE_ADDR'])

	try:
		mess = Message.objects.get(message_id = param_message_hash)
	except Message.DoesNotExist:
		raise Http404

	try:
		contact = Recipient.objects.get(tracking_id = param_recipient_hash)
	except Recipient.DoesNotExist:
		raise Http404

	Event.objects.create(	ip_address = request.META['REMOTE_ADDR'], latitude = coordinates['latitude'],
							longitude = coordinates['longitude'], country_code = coordinates['country_code'],
							recipient = contact, message = mess )

	image = open("/home/kgluce/mailprime/mailprime/static/images/icon.png").read()
	return HttpResponse(image, content_type="image/png")

def tracker_unsubscribe(request, param_recipient_hash):
	try:
		contact = Recipient.objects.get(tracking_id = param_recipient_hash)
	except Recipient.DoesNotExist:
		raise Http404

	# Get Campaign, and increment unsub count
	campaign = contact.campaign
	campaign.unsub_count += 1
	campaign.save()

	# Delete the recipient from the database
	contact.delete()

	# Generate message that will be displayed to the user
	messages.add_message(request, messages.SUCCESS, 'You have successfully unsubscribed!')
	return HttpResponseRedirect('/')

def tracker_authorize(request, param_recipient_hash):
	try:
		contact = Recipient.objects.get(tracking_id = param_recipient_hash)
	except Recipient.DoesNotExist:
		raise Http404

	contact.active = True
	contact.save()

	messages.add_message(request, messages.SUCCESS, 'You have sucessfully subscribed. Thank You!')
	return HttpResponseRedirect('/')