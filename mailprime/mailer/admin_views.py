from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import RequestContext
from mailer.lib import authenticate_user, current_user, current_staff, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from mailer.models import Send_Event, Event, Profile
from mailer.forms import UserProfileForm


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

		return render(request, 'administrative/index.html', page_vars)

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

def users(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'All Users'}

		page_vars['users'] = User.objects.all().order_by('last_login')

		return render(request, 'administrative/users.html', page_vars)

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

		return render(request, 'administrative/edit_user.html', page_vars)

	else:
		raise Http404
