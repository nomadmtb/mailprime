from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from django.http import Http404
from mailer.forms import CampaignForm, MessageForm, LoginForm, UserProfileForm
import pytz
from django.utils import timezone

# Homepage for the application
def index(request):
	data = { "page_title": "Mailpri.me"}
	return render( request, 'index.html', data)

# The login page for the application.
def login(request):
	page_vars = { "page_title": "login" }

	if request.method == 'POST':

		if authenticate_user(request, request.POST['username'], request.POST['password']):
			user_profile = Profile.objects.filter(user = request.user)

			# Create Profile if User doesn't have one.
			if not user_profile:
				Profile(time_zone="UTC", user=request.user).save()

			return HttpResponseRedirect('/' + request.user.username + '/campaigns')
		else:
			return HttpResponseRedirect('/login')
	elif request.method == 'GET':
		if current_user(request):
			return HttpResponseRedirect('/')
		else:
			page_vars['form'] = LoginForm()
			csrfContext = RequestContext(request, page_vars)
			return render(request, 'auth/login.html', csrfContext)

# The logout view that will logout the user.
def logout(request):
	if logout_user(request):
		return HttpResponseRedirect('/')

def terms_of_service(request):
	return render(request, 'terms_of_service.html')

# The user account view that will display/update user information.
def user_account(request, param_username):
	page_vars = { "page_title": "Account: " + request.user.username }

	if current_user(request) and param_username == request.user.username:

		try:
			requested_user = User.objects.get(username=param_username)
		except User.DoesNotExist:
			raise Http404

		if request.method == "GET":
			user_profile = Profile.objects.get(user = request.user)
			init_values = {'time_zone': user_profile.time_zone, 'email': request.user.email}
			page_vars['form'] = UserProfileForm(initial=init_values)
			csrfContext = RequestContext(request, page_vars)
			
			return render(request, 'auth/user_account.html', csrfContext)

		elif request.method == "POST":
			if current_user(request):
				completed_form = UserProfileForm(request.POST)

				if completed_form.is_valid():

					user_profile = Profile.objects.get(user=request.user)
					user_obj = User.objects.get(username=request.user.username)

					# Updating User and Profile Objects with form data
					user_profile.time_zone = completed_form.cleaned_data['time_zone']

					request.session['user_timezone'] = completed_form.cleaned_data['time_zone']

					user_obj.email = completed_form.cleaned_data['email']

					# Only update the user's password if it's not empty
					if completed_form.cleaned_data['password'] != '':
						user_obj.set_password(completed_form.cleaned_data['password'])

					# Commiting the edited objects to the database
					user_profile.save()
					user_obj.save()

					messages.add_message(request, messages.SUCCESS, 'Success: Your Account Has Been Updated')
					return HttpResponseRedirect('/' + request.user.username + '/account')
				else:
					generate_form_errors(request, completed_form)
					return HttpResponseRedirect('/' + request.user.username + '/account')
			else:
				raise Http404
		
	else:
		raise Http404