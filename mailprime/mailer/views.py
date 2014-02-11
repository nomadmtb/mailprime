from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user
from django.http import HttpResponseRedirect
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages


def index(request):
	data = { "page_title": "Mailpri.me"}
	return render( request, 'index.html', data)

def login(request):
	data = { "page_title": "login" }
	csrfContext = RequestContext(request, data)

	if request.method == 'POST':
		if authenticate_user(request, request.POST['username'], request.POST['password']):
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/login')
	else:
		return render(request, 'login.html', csrfContext)

def logout(request):
	if logout_user(request):
		return HttpResponseRedirect('/')

def home(request):
	if current_user(request):
		user_campaigns = Campaign.objects.filter(user=request.user)
		page_vars = {"user_campaigns": user_campaigns, "page_title": "My Campaigns"}
		return render(request, 'home.html', page_vars)

	else:
		return HttpResponseRedirect('/login')

def user_account(request, param_username):
	page_vars = { "page_title": "Account: " + request.user.username }

	if current_user(request):

		try:
			requested_user = User.objects.get(username=param_username)
		except User.DoesNotExist:
			messages.add_message(request, messages.WARNING, "Something went wrong")
			return HttpResponseRedirect('/')
			
		if requested_user.username == request.user.username:
			page_vars['user'] = request.user
			return render(request, 'user_account.html', page_vars)
		else:
			messages.add_message(request, messages.WARNING, "Don\'t Be Bad")
			return HttpResponseRedirect('/')
	else:
		return HttpResponseRedirect('/')

def user_campaigns(request, param_username):
	page_vars = { "page_title": request.user.username + '\'s campaigns' }

	if current_user(request) and param_username == request.user.username:
		user_campaigns = Campaign.objects.filter(user = request.user)
		page_vars['campaigns'] = user_campaigns
		return render(request, 'user_campaigns.html', page_vars)
	else:
		messages.add_message(request, messages.WARNING, "Something went wrong")
		return HttpResponseRedirect('/') # HTTP_404

def user_campaign(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign View'}

	if current_user(request) and request.user.username == param_username:

		try:
			user_campaign = Campaign.objects.get(pk = param_campaign_pk)
		except Campaign.DoesNotExist:
			messages.add_message(request, messages.WARNING, "Something went wrong")
			return HttpResponseRedirect('/') # HTTP_404

		page_vars['campaign'] = user_campaign
		return render(request, 'user_campaign.html', page_vars)

	else:
		messages.add_message(request, messages.WARNING, "Something went wrong")
		return HttpResponseRedirect('/') # HTTP_404

def user_campaign_recipients(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign Recipients'}

	if current_user(request) and request.user.username == param_username:
		recipients = Recipient.objects.filter(campaign__pk = param_campaign_pk)
		page_vars['recipients'] = recipients
		return render(request, 'user_campaign_recipients.html', page_vars)
	else:
		messages.add_message(request, messages.WARNING, "Something went wrong")
		return HttpResponseRedirect('/') # HTTP_404

def user_campaign_messages(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign Messages'}

	if current_user(request) and request.user.username == param_username:
		campaign_messages = Message.objects.filter(campaign__pk = param_campaign_pk)
		page_vars['messages'] = campaign_messages
		return render(request, 'user_campaign_messages.html', page_vars)
	else:
		messages.add_message(request, messages.WARNING, "Something went wrong")
		return HttpResponseRedirect('/') # HTTP_404

def user_campaign_message(request, param_username, param_campaign_pk, param_message_pk):
	page_vars = {"page_title": 'Campaign Message'}

	if current_user(request) and request.user.username == param_username:
		try:
			message = Message.objects.get(campaign__pk = param_campaign_pk, campaign__user__username = request.user.username, pk = param_message_pk)
		except Message.DoesNotExist:
			messages.add_message(request, messages.WARNING, "Something went wrong")
			return HttpResponseRedirect('/') # HTTP_404
		page_vars['message'] = message
		return render(request, 'user_campaign_message.html', page_vars)

def campaign(request, campaign_id):
	if current_user(request):
		user_campaign = Campaign.objects.get(user=request.user, pk=campaign_id)
		page_vars = {"campaign": user_campaign, "page_title": user_campaign.title }
		return render(request, 'campaign.html', page_vars)
	else:
		return HttpResponseRedirect('/login')