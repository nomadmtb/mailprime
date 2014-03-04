from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user, current_user, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse
from mailer.models import Profile, Campaign, Recipient, Event, Message
from django.contrib import messages
from django.http import Http404
from mailer.forms import CampaignForm, MessageForm, LoginForm, ProfileForm

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
				Profile(public_email=request.user.email, agree_terms=False, time_zone=0, user=request.user).save()

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
			page_vars['form'] = ProfileForm(instance=requested_user.profile)
			csrfContext = RequestContext(request, page_vars)
			
			return render(request, 'auth/user_account.html', csrfContext)
		
	else:
		raise Http404