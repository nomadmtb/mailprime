from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse, Http404
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from mailer.forms import CampaignForm

# The user campaigns view that will show all of the campaigns belonging to the user.
def user_campaigns(request, param_username):
	page_vars = { "page_title": request.user.username + '\'s campaigns' }

	if current_user(request) and param_username == request.user.username:
		user_campaigns = Campaign.objects.filter(user = request.user).order_by('-created_date')
		page_vars['campaigns'] = user_campaigns
		return render(request, 'campaign/index.html', page_vars)
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

		if user_campaign.user.username != request.user.username:
			raise Http404

		if user_campaign.active == False:
			messages.add_message(request, messages.ERROR, 'Campaign disabled by MailPrime Administrator')

		page_vars['campaign'] = user_campaign
		page_vars['message_count'] = Message.objects.filter(campaign = user_campaign).count()
		page_vars['recipient_count'] = Recipient.objects.filter(campaign = user_campaign).count()
		return render(request, 'campaign/show.html', page_vars)
	else:
		raise Http404

def user_campaign_new(request, param_username):
	if current_user(request) and request.user.username == param_username:
		page_vars = {"page_title": "New Campaign"}

		if request.method == 'POST':

			completed_form = CampaignForm(request.POST)

			if completed_form.is_valid():

				campaign = completed_form.save(commit=False)
				campaign.user = request.user
				campaign.active = True
				campaign.save()

				messages.add_message(request, messages.SUCCESS, 'Created New Campaign')

				return HttpResponseRedirect('/' + request.user.username + '/campaign-' + str(campaign.pk))
			else:
				generate_form_errors(request, completed_form)
				page_vars['form'] = completed_form
				return render(request, 'campaign/new.html', page_vars)
				
		elif request.method == "GET":
			page_vars['form'] = CampaignForm()
			csrfContext = RequestContext(request, page_vars)
			return render(request, 'campaign/new.html', csrfContext)
	else:
		raise Http404

def user_campaign_edit(request, param_username, param_campaign_pk):
	page_vars = {"page_title": "Edit Campaign"}

	if current_user(request) and param_username == request.user.username:
		try:
			user_campaign = Campaign.objects.get(pk = param_campaign_pk)
		except Campaign.DoesNotExist:
			raise Http404

		if user_campaign.user != request.user:
			raise Http404

		page_vars['campaign'] = user_campaign

		if user_campaign.user == request.user:

			if request.method == "GET":
				action = request.GET.get('action')

				if action == "delete":
					# We want to delete the campaign
					Campaign.objects.filter(pk=param_campaign_pk).delete()
					messages.add_message(request, messages.SUCCESS, 'Successfully deleted Campaign')
					return HttpResponseRedirect('/' + request.user.username + '/campaigns')

				else:
					# We want to edit the campaign, render form				
					page_vars['form'] = CampaignForm(instance=user_campaign)

					# Generate warning is campaign is disabled
					if user_campaign.active == False:
						messages.add_message(request, messages.ERROR, 'Campaign disabled by MailPrime Administrator')

					# Generate CSRF Context
					csrfContext = RequestContext(request, page_vars)

					# Render page for user
					return render(request, 'campaign/edit.html', csrfContext)

			elif request.method == "POST":

				# Check if campaign is disabled
				if user_campaign.active == False:
					return HttpResponseRedirect('/{0}/campaign-{1}'.format(request.user.username, user_campaign.pk))

				# It's safe to assume that the campaign is active, process form
				completed_form = CampaignForm(request.POST, instance=user_campaign)

				if completed_form.is_valid():
					completed_form.save()
					messages.add_message(request, messages.SUCCESS, 'Successfully Updated Campaign')
					return HttpResponseRedirect('/' + request.user.username + '/campaign-' + str(user_campaign.pk))
				else:
					generate_form_errors(request, completed_form)
					page_vars['form'] = completed_form
					return render(request, 'campaign/edit.html', page_vars)
