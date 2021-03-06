from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from django.http import Http404
from mailer.forms import CampaignForm, MessageForm, LoginForm, RecipientForm, ContactUploadForm
from django.core.validators import validate_email
from django import forms
from django.db import IntegrityError
import os

# The user campaign recipients view will show all users that are associated with a particular campaign.
def user_campaign_recipients(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Campaign Recipients'}

	if current_user(request) and request.user.username == param_username:

		try:
			campaign = Campaign.objects.get(pk = param_campaign_pk, user=request.user)
		except Campaign.DoesNotExist:
			raise Http404

		recipients = Recipient.objects.filter(campaign = campaign).order_by('email')

		# Checking to see if the campaign is disabled
		if campaign.active:

			# Looking for the 'delete' GET parameter, so we can remove the recipient
			recipient_to_remove = request.GET.get('delete')
			print recipient_to_remove

			# Check to make sure, recip_pk belongs to campaign.
			# If so, delete it from the database.
			if recipient_to_remove is not None:

				for x in recipients:

					if int(recipient_to_remove) == x.pk:

						messages.add_message(request, messages.SUCCESS, 'Successfully Removed {0}'.format( x.email ))
						x.delete()

						# Update recipients queryset
						recipients = Recipient.objects.filter(campaign = campaign).order_by('email')
		else:

			# Generate warning because campaign is disabled
			messages.add_message(request, messages.SUCCESS, 'Campaign disabled by MailPrime Administrator')

		# Page varaibles and render page
		page_vars['campaign'] = campaign
		page_vars['recipients'] = recipients

		return render(request, 'recipient/index.html', page_vars)

	else:
		
		raise Http404

def upload_recipients(request, param_username, param_campaign_pk):
	page_vars = {"page_title": 'Upload Recipients'}

	if current_user(request) and request.user.username == param_username:

		# Capturing Campaign that will be used with the recipient entries
		try:
			campaign = Campaign.objects.get(pk=param_campaign_pk, user=request.user)
		except Campaign.DoesNotExist:
			raise Http404

		# User is requesting page, render form
		if request.method == 'GET':

			page_vars['campaign'] = campaign
			page_vars['form'] = ContactUploadForm()
			
			csrfContext = RequestContext(request, page_vars)
			return render(request, 'recipient/upload.html', csrfContext)

		# User is uploading from form, parse data
		elif request.method == 'POST':

			# Check to see if campaign is disabled
			if campaign.active == False:

				#Generate warning, redirect.
				messages.add_message(request, messages.SUCCESS, 'Campaign disabled by MailPrime Administrator')
				return HttpResponseRedirect('/{0}/campaign-{1}/recipients/upload'.format(request.user.username, campaign.pk))

			# Can be assumed that the campaign is not disabled now

			# Page Vars
			page_vars = { 'page_title': 'Upload Report'}

			# Array that will contain invalid/valid emails
			invalid_emails = {}
			valid_emails = {}

			# Valid email flag
			valid = True
			valid_recip = True
			valid_email_count = 0
			invalid_email_count = 0

			form = ContactUploadForm(request.POST, request.FILES)

			if form.is_valid():

				uploaded_file = request.FILES['contact_file']

				# Splitting file into chunks so it doesn't eat up system resources
				for chunk in uploaded_file.chunks():

					# Iterate through each line
					for line in chunk.rstrip().split('\n'):

						try:
							validate_email(line)
						except forms.ValidationError:
							valid = False

						if valid:

							# Save new Recipient to database
							try:
								Recipient(email=line, campaign=campaign).save()
							except IntegrityError:
								valid_recip = False


							# Increment counter
							if (valid_recip):

								valid_email_count += 1
								valid_emails[line] = 'Success'

							else:

								invalid_email_count += 1
								invalid_emails[line] = 'Repeated'

						else:

							# Increment counter
							invalid_email_count += 1
							invalid_emails[line] = 'Invalid'

						# Reset valid flag
						valid = True
						valid_recip = True

				# Giving campaign to template for URL reasons
				page_vars['campaign'] = campaign

				# Generate messages for user
				if (valid_email_count > 0):
					messages.add_message(request, messages.SUCCESS, "{0} Successful Entries".format(valid_email_count))
					page_vars['valid_emails'] = valid_emails

				if (invalid_email_count > 0):
					messages.add_message(request, messages.SUCCESS, "{0} Entries Failed".format(invalid_email_count))
					page_vars['invalid_emails'] = invalid_emails

				# Send out Invitations if necessary
				if valid_email_count > 0:
					os.system("python /var/www/mailprime/manage.py deploy_invitations {0} &".format(campaign.pk))

				return render(request, 'recipient/upload_report.html', page_vars)

			# Form is NOT valid
			else:
				generate_form_errors(request, form)
				return HttpResponseRedirect('/{0}/campaign-{1}/recipients/upload'.format( request.user.username, campaign.pk ))
				
	else:
		raise Http404

def add_recipient(request, param_username, param_campaign_pk):
	if current_user(request) and request.user.username == param_username:
		page_vars = {'page_title': 'Add Recipient'}

		try:
			page_vars['campaign'] = Campaign.objects.get(pk=param_campaign_pk, user=request.user)
		except Campaign.DoesNotExist:
			raise Http404

		# User is requesting page
		if request.method == "GET":
			page_vars['form'] = RecipientForm()

			csrfContext = RequestContext(request, page_vars)
			return render(request, 'recipient/add.html', csrfContext)

		# User is uploading from the form
		elif request.method == "POST":

			# Check to see if the campaign is disabled
			if page_vars['campaign'].active:
				completed_form = RecipientForm(request.POST)

				if completed_form.is_valid():
					recipient = completed_form.save(commit=False)

					recipient.campaign = page_vars['campaign']
					recipient.save()

					# Send out invitation!!!
					os.system("python /var/www/mailprime/manage.py deploy_invitations {0} &".format( recipient.campaign.pk ))
					
					return HttpResponseRedirect('/' + request.user.username + '/campaign-' + str(page_vars['campaign'].pk) + '/recipients')
				else:
					generate_form_errors(request, completed_form)
					page_vars['form'] = completed_form
					return render(request, 'recipient/add.html', page_vars)

			else:

				# Campaign is deactivated, generate message.
				messages.add_message(request, messages.SUCCESS, 'Campaign disabled by MailPrime Administrator')
				return HttpResponseRedirect('/{0}/campaign-{1}/recipients/add'.format(request.user.username, page_vars['campaign'].pk))

	else:
		raise Http404
