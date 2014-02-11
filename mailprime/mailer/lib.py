# This file will contain extra 'helper' functions.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout

def authenticate_user(request, username, password):
	user = authenticate(username=username, password=password)

	if user is not None:
		if user.is_active:
			login(request, user)
			messages.add_message(request, messages.SUCCESS, 'Welcome, ' + user.username)
			return True
		else:
			messages.add_message(request, messages.WARNING, 'Your account has been disabled')
			return False
	else:
		messages.add_message(request, messages.WARNING, 'Invalid Credentials')
		return False

def current_user(request):
	if request.user.is_authenticated():
		return True
	else:
		messages.add_message(request, messages.WARNING, 'You must be logged in')
		return False

def logout_user(request):
	logout(request)
	messages.add_message(request, messages.INFO, 'You have successfully logged out')
	return True
