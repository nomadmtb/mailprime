from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import RequestContext
from mailer.lib import authenticate_user, current_user, current_staff, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from mailer.models import Send_Event, Event, Profile, Message, Campaign
from mailer.forms import UserProfileForm, AdminMessageForm, AdminCampaignForm, AdminCreateUserForm


# Index page for administrative area.
def index(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'Administrative Interface'}

		# Getting recent send_events. Limit to 25 max.
		page_vars['send_events'] = Send_Event.objects.all().order_by('-send_date')[:25]
		page_vars['send_event_count'] = Send_Event.objects.count()

		# Getting recent users. Limit to 25 max.
		page_vars['users'] = User.objects.all().order_by('-last_login')[:25]
		page_vars['user_count'] = User.objects.count()

		# Getting recent 'read' events. Limit to 25 max.
		page_vars['events'] = Event.objects.all().order_by('-created_date')[:25]
		page_vars['event_count'] = Event.objects.count()

		# Getting recent messages. Limit to 25 max.
		page_vars['user_messages'] = Message.objects.all().order_by('-created_date')[:25]
		page_vars['user_message_count'] = Message.objects.count()

		# Getting recent campaigns. Limit to 25 max.
		page_vars['campaigns'] = Campaign.objects.all().order_by('-created_date')[:25]
		page_vars['campaign_count'] = Campaign.objects.count()

		return render(request, 'administrative/index.html', page_vars)

	else:
		raise Http404

def show_campaigns(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'All Campaigns'}

		# Getting all Campaigns from the database.
		page_vars['campaigns'] = Campaign.objects.all().order_by('-created_date')

		# Render html template for user.
		return render(request, 'administrative/campaigns.html', page_vars)

	else:
		raise Http404

def send_events(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'All Send Events'}

		page_vars['send_events'] = Send_Event.objects.all().order_by('-send_date')

		return render(request, 'administrative/send_events.html', page_vars)

	else:
		raise Http404

def show_users(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'All Users'}

		page_vars['users'] = User.objects.all().order_by('-last_login')

		return render(request, 'administrative/users.html', page_vars)

	else:
		raise Http404

def show_messages(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'All Messages'}

		page_vars['user_messages'] = Message.objects.all().order_by('-created_date')

		return render(request, 'administrative/messages.html', page_vars)

	else:
		raise Http404

def edit_campaign(request, param_campaign_pk):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'Alter Campaign'}

		# Get Campaign object from database.
		try:
			requested_campaign = Campaign.objects.get(pk=param_campaign_pk)
		except Campaign.DoesNotExist:
			raise Http404

		# User is requesting the form, build it!
		if request.method == "GET":

			# Build form with requested campaign.
			page_vars['form'] = AdminCampaignForm(instance=requested_campaign)
			page_vars['requested_campaign'] = requested_campaign

			# Build CSRF context.
			csrfContext = RequestContext(request, page_vars)

			# Render page.
			return render(request, 'administrative/edit_campaign.html', csrfContext)

		# User is submitting the form, update it!
		elif request.method == "POST":

			# Build campaignform object from post data.
			completed_form = AdminCampaignForm(request.POST, instance=requested_campaign)

			# Save campaign if it's valid.
			if completed_form.is_valid():

				# Commit changes to database.
				completed_form.save()

				# Generate message for user.
				messages.add_message(request, messages.SUCCESS, 'Success: Changes Applied to Campaign')

				# Redirect back to edit page.
				return HttpResponseRedirect("/admin/edit_campaign/{0}".format(requested_campaign.pk))

			# Form is not valid!
			else:
				raise Http404

	else:
		raise Http404

def edit_message(request, param_message_pk):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'Alter Message'}

		# Get Message object from database.
		try:
			requested_message = Message.objects.get(pk=param_message_pk)
		except Message.DoesNotExist:
			raise Http404

		# User is requesting the form, build it!
		if request.method == "GET":
			
			# Build form with requested message.
			page_vars['form'] = AdminMessageForm(instance=requested_message)
			page_vars['requested_message'] = requested_message

			# Build CSRF context.
			csrfContext = RequestContext(request, page_vars)

			# Render page.
			return render(request, 'administrative/edit_message.html', csrfContext)

		# User is submitting the form, apply it!
		elif request.method == "POST":

			# Build messageform object from post data.
			completed_form = AdminMessageForm(request.POST, instance=requested_message)

			# Save message if it passes validation.
			if completed_form.is_valid():

				# Commit to database.
				completed_form.save()

				# Generate message for user.
				messages.add_message(request, messages.SUCCESS, 'Success: Changes Applied to Message')

				# Redirect user back to edit page.
				return HttpResponseRedirect('/admin/edit_message/{0}'.format(requested_message.pk))

			else:
				raise Http404

	else:
		raise Http404

def add_user(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'Add User'}

		# User is requesting form, build it!
		if request.method == "GET":

			# Build form object.
			page_vars['form'] = AdminCreateUserForm()

			# Generating CSRF Context.
			csrfContext = RequestContext(request, page_vars)

			# Render page for user.
			return render(request, 'administrative/add_user.html', csrfContext)

		# User is submitting form, process it!
		elif request.method == "POST":

			# Build form object from post data.
			completed_form = AdminCreateUserForm(request.POST)

			# If form validates correctly, save.
			if completed_form.is_valid():

				# Saving new user to database.
				new_user = completed_form.save(commit=False)
				new_user.save()

				# We want to create a new Profile for the user too!
				new_profile = Profile(user=new_user, time_zone='UTC', agree_terms=False)
				new_profile.save()

				# Generate message for user.
				messages.add_message(request, messages.SUCCESS, 'Success: New User Added')

				# Redirect back to admin page.
				return HttpResponseRedirect('/admin')

			# Form is NOT valid.
			else:

				# Form is not valid, re-render the page with the form.
				generate_form_errors(request, completed_form)
				page_vars['form'] = completed_form

				# Generate CSRF Context.
				csrfContext = RequestContext(request, page_vars)

				# Render page for user.
				return render(request, 'administrative/add_user.html', csrfContext)

	else:
		raise Http404


def edit_user(request, param_user_pk):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'Alter User'}

		# Getting Requested User object from database.
		try:
			requested_user = User.objects.get(pk=param_user_pk)
		except User.DoesNotExist:
			raise Http404

		# User is requesting the form, build it!
		if request.method == "GET":

			# Get profile object from database.
			try:
				user_profile = Profile.objects.get(user=requested_user)
			except Profile.DoesNotExist:
				raise Http404

			# Build initial values for form.
			init_values = {'agree_terms': user_profile.agree_terms, 'time_zone': user_profile.time_zone, 'email': requested_user.email}

			# Create Form object with initial values.
			page_vars['form'] = UserProfileForm(initial=init_values)

			# Getting requested_user so we can create the post link via pk.
			page_vars['requested_user'] = requested_user

			# Generating the CSRF context.
			csrfContext = RequestContext(request, page_vars)

			# Render page with form.
			return render(request, 'administrative/edit_user.html', csrfContext)

		# Okay so the user is submitting changes, apply them!
		elif request.method == "POST":

			# Build form obj from POST data.
			completed_form = UserProfileForm(request.POST)

			if completed_form.is_valid():

				# We need to get the profile obj out of the db.
				try:
					user_profile = Profile.objects.get(user=requested_user)
				except Profile.DoesNotExist:
					raise Http404

				# Update User and Profile objs in db with validated form-data.
				user_profile.time_zone = completed_form.cleaned_data['time_zone']
				user_profile.agree_terms = completed_form.cleaned_data['agree_terms']
				requested_user.email = completed_form.cleaned_data['email']

				# Only update the password if it's not empty.
				if completed_form.cleaned_data['password'] != '':
					requested_user.set_password(completed_form.cleaned_data['password'])

				# Save the changes to the database.
				user_profile.save()
				requested_user.save()

				# Generate message for the user
				messages.add_message(request, messages.SUCCESS, 'Success: Changes Applied to User')

				# Redirect back to user-edit page.
				return HttpResponseRedirect('/admin/edit_user/{0}'.format(requested_user.pk))

			# Form data is NOT valid. Generate messages.
			else:

				# Generate error messages from form
				generate_form_errors(request, completed_form)

				# Update page_vars
				page_vars['form'] = completed_form

				# Generate CSRF Context.
				csrfContext = RequestContext(request, page_vars)

				# Render page with errors, old form.
				return render(request, 'administrative/edit_user.html', csrfContext)

	else:
		raise Http404
