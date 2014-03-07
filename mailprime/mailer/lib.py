# This file will contain extra 'helper' functions.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
import requests
import os

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
		return False

def logout_user(request):
	logout(request)
	messages.add_message(request, messages.INFO, 'You have successfully logged out')
	return True

def generate_form_errors(request, form):
	# For ValidationErrors that are not associated with a particular form field.
	for entry in form.non_field_errors():
		messages.add_message(request, messages.ERROR, entry)

	# For Errors associated with a particular form field.
	for field in form:
		for error in field.errors:
			messages.add_message(request, messages.ERROR, 'ERROR: ' + unicode(field.label) + ', ' + unicode(error))
	return request

def geo_locate(param_ip_address):
	coordinates = {}
	response = requests.get('http://freegeoip.net/json/' + param_ip_address).json()

	if response[u'latitude'] and response[u'longitude'] == 0:
		coordinates['latitude'] = None
		coordinates['longitude'] = None
	else:
		coordinates['latitude'] = response[u'latitude']
		coordinates['longitude'] = response[u'longitude']

	return coordinates

def send_messages(param_messages):
	for message in param_messages:
		command = 'echo "{0}" | mail -a "Content-type: multipart/mixed; boundary=\"mess_bound\"" -a "MIME-Version: 1.0" -s "{1}" {2}'.format(message['message'], message['subject'], message['to'])
		os.system(command)