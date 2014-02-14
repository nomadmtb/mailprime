from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate
from django.http import HttpResponseRedirect, HttpResponse
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from django.http import Http404

# Homepage for the application
def index(request):
	data = { "page_title": "Mailpri.me"}
	return render( request, 'index.html', data)

# The login page for the application.
def login(request):
	data = { "page_title": "login" }
	csrfContext = RequestContext(request, data)

	if request.method == 'POST':
		if authenticate_user(request, request.POST['username'], request.POST['password']):
			return HttpResponseRedirect('/' + request.user.username + '/campaigns')
		else:
			return HttpResponseRedirect('/login')
	else:
		return render(request, 'login.html', csrfContext)

# The logout view that will logout the user.
def logout(request):
	if logout_user(request):
		return HttpResponseRedirect('/')

# The user account view that will display/update user information.
def user_account(request, param_username):
	page_vars = { "page_title": "Account: " + request.user.username }

	if current_user(request):

		try:
			requested_user = User.objects.get(username=param_username)
		except User.DoesNotExist:
			raise Http404
			
		if requested_user.username == request.user.username:
			page_vars['user'] = request.user
			return render(request, 'user_account.html', page_vars)
		else:
			raise Http404
	else:
		raise Http404

# The user campaigns view that will show all of the campaigns belonging to the user.
def user_campaigns(request, param_username):
	page_vars = { "page_title": request.user.username + '\'s campaigns' }

	if current_user(request) and param_username == request.user.username:
		user_campaigns = Campaign.objects.filter(user = request.user)
		page_vars['campaigns'] = user_campaigns
		return render(request, 'user_campaigns.html', page_vars)
	else:
		raise Http404

# The user campaign view will show the campaign data belonging to a PARTICULAR user.
def user_campaign(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign View'}

	if current_user(request) and request.user.username == param_username:

		try:
			user_campaign = Campaign.objects.get(pk = param_campaign_pk)
		except Campaign.DoesNotExist:
			raise Http404

		page_vars['campaign'] = user_campaign
		return render(request, 'user_campaign.html', page_vars)
	else:
		raise Http404

# The user campaign recipients view will show all users that are associated with a particular campaign.
def user_campaign_recipients(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign Recipients'}

	if current_user(request) and request.user.username == param_username:
		recipients = Recipient.objects.filter(campaign__pk = param_campaign_pk)
		page_vars['recipients'] = recipients
		return render(request, 'user_campaign_recipients.html', page_vars)
	else:
		raise Http404

# The user campaigns messages view will show the messages that belong to a specific campaign.
def user_campaign_messages(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign Messages'}

	if current_user(request) and request.user.username == param_username:
		campaign_messages = Message.objects.filter(campaign__pk = param_campaign_pk)
		page_vars['campaign_messages'] = campaign_messages
		return render(request, 'user_campaign_messages.html', page_vars)
	else:
		raise Http404

# The user campaign view will show all of the data that belongs to a specific message.
def user_campaign_message(request, param_username, param_campaign_pk, param_message_pk):
	page_vars = {"page_title": 'Campaign Message'}

	if current_user(request) and request.user.username == param_username:

		try:
			message = Message.objects.get(campaign__pk = param_campaign_pk, campaign__user__username = request.user.username, pk = param_message_pk)
		except Message.DoesNotExist:
			raise Http404

		page_vars['message'] = message
		return render(request, 'user_campaign_message.html', page_vars)

	else:
		raise Http404

# The user-campaign-message-events-view will show all of the events associated with a particular message
def user_campaign_message_events(request, param_username, param_campaign_pk, param_message_pk):
	page_vars = {"page_title": 'Message Events'}

	if current_user(request) and request.user.username == param_username:
		events = Event.objects.filter(message__campaign__pk = param_campaign_pk, message__pk = param_message_pk)
		page_vars['events'] = events
		return render(request, 'user_campaign_message_events.html', page_vars)
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
		return render(request, 'user_campaign_message_event.html', page_vars)
	else:
		raise Http404

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

	Event.objects.create(ip_address = request.META['REMOTE_ADDR'], latitude = coordinates['latitude'], longitude = coordinates['longitude'], recipient = contact, message = mess)

	image = open("/Users/kgluce/Documents/programming/django/mailprime/mailprime/static/images/circle.jpg").read()
	return HttpResponse(image, content_type="image/jpg")

def tracker_unsubscribe(request, param_recipient_hash):
	try:
		contact = Recipient.objects.get(tracking_id = param_recipient_hash)
	except Recipient.DoesNotExist:
		raise Http404

	contact.delete()
	messages.add_message(request, messages.SUCCESS, 'You have successfully unsubscribed!')
	return HttpResponseRedirect('/')

def message_statistics(request, param_username, param_campaign_pk, param_message_pk):
	page_vars = {}
	page_vars['page_title'] = 'Message Statistics'

	return render(request, 'message_statistics.html', page_vars)

def campaign_statistics(request, param_username, param_campaign_pk):
	page_vars = {}
	page_vars['page_title'] = 'Campaign Statistics'

	return render(request, 'campaign_statistics.html', page_vars)