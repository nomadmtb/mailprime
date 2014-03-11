from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from django.http import Http404
from mailer.forms import CampaignForm, MessageForm, LoginForm

# The user campaigns messages view will show the messages that belong to a specific campaign.
def user_campaign_messages(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign Messages'}

	try:
		campaign = Campaign.objects.get(pk = param_campaign_pk)
	except Campaign.DoesNotExist:
		raise Http404

	if campaign.user.username != request.user.username:
		raise Http404

	page_vars['campaign'] = campaign;

	if current_user(request) and request.user.username == param_username:
		campaign_messages = Message.objects.filter(campaign__pk = param_campaign_pk).order_by('-created_date')
		page_vars['campaign_messages'] = campaign_messages
		return render(request, 'message/index.html', page_vars)
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

		deploy = request.GET.get('deploy')

		if (deploy is not None) and (deploy == message.pk):
			os.system("./deploy_messages.py " + str(message.pk) + "&")
			messages.add_message(request, messages.SUCCESS, 'You Message Has Been Deployed')
			return HttpResponseRedirect('/' + request.user.username + '/campaign-' + str(message.campaign.pk) + '/messages')

		page_vars['message'] = message
		return render(request, 'message/show.html', page_vars)

	else:
		raise Http404

def user_campaign_message_new(request, param_username, param_campaign_pk):
	if current_user(request) and request.user.username == param_username:

		try:
			campaign = Campaign.objects.get(pk = param_campaign_pk)
		except Campaign.DoesNotExist:
			raise Http404

		if campaign.user == request.user:
			page_vars = {"page_title": "New Message"}
			page_vars['campaign'] = campaign

			if request.method == "POST":
				
				completed_form = MessageForm(request.POST)

				if completed_form.is_valid():
					message = completed_form.save(commit=False)
					message.campaign_id = param_campaign_pk
					message.save()
					return HttpResponseRedirect('/'+ request.user.username + "/campaign-" + str(message.campaign.id) + "/messages")
				else:
					generate_form_errors(request, completed_form)
					page_vars['form'] = completed_form
					return render(request, 'message/new.html', page_vars)
			else:
				# Process GET DATA...
				page_vars['form'] = MessageForm()
				csrfContext = RequestContext(request, page_vars)
				return render(request, 'message/new.html', csrfContext)
	else:
		raise Http404

def message_statistics(request, param_username, param_campaign_pk, param_message_pk):
	page_vars = {}
	page_vars['page_title'] = 'Message Statistics'

	return render(request, 'message/stats.html', page_vars)