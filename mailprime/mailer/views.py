from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user
from django.http import HttpResponseRedirect
from mailer.models import Profile, Campaign, Recipient, Event, Message

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

def campaign(request, campaign_id):
	user_campaign = Campaign.objects.get(user=request.user, pk=campaign_id)
	page_vars = {"campaign": user_campaign, "page_title": user_campaign.title }
	return render(request, 'campaign.html', page_vars)