from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from django.http import Http404
from mailer.forms import CampaignForm, MessageForm, LoginForm, RecipientForm

# The user campaign recipients view will show all users that are associated with a particular campaign.
def user_campaign_recipients(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign Recipients'}

	if current_user(request) and request.user.username == param_username:
		recipients = Recipient.objects.filter(campaign__pk = param_campaign_pk).order_by('email')
		page_vars['recipients'] = recipients
		return render(request, 'recipient/index.html', page_vars)
	else:
		raise Http404

def upload_recipients(request, param_username, param_campaign_pk):
	pass

def add_recipient(request, param_username, param_campaign_pk):
	if current_user(request) and request.user.username == param_username:
		if request.method == "GET":
			page_vars = {"page_title": "Add Recipient"}
			page_vars['form'] = RecipientForm()

			try:
				page_vars['campaign'] = Campaign.objects.get(pk=param_campaign_pk, user=request.user)
			except Campaign.DoesNotExist:
				raise Http404

			csrfContext = RequestContext(request, page_vars)
			return render(request, 'recipient/add.html', csrfContext)
		elif request.method == "POST":
			completed_form = RecipientForm(request.POST)

			if completed_form.is_valid():
				recipient = completed_form.save(commit=False)

				try:
					campaign = Campaign.objects.get(pk=param_campaign_pk, user=request.user)
				except Campaign.DoesNotExist:
					raise Http404

				recipient.campaign = campaign

				# Send out invitation!!!
				recipient.save()
				return HttpResponseRedirect('/' + request.user.username + '/campaign-' + str(campaign.pk) + '/recipients')
			else:
				generate_form_errors(request, completed_form)
				page_vars['form'] = completed_form
				return render(request, 'recipient/add.html', page_vars)
	else:
		raise Http404