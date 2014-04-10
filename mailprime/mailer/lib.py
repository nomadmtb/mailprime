# This file will contain extra 'helper' functions.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout
from django.core import mail
import requests
import os
import time

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

	# Checking for valid Geo-Coordinates
	if response[u'latitude'] == 0 and response[u'longitude'] == 0:
		coordinates['latitude'] = None
		coordinates['longitude'] = None
	else:
		coordinates['latitude'] = response[u'latitude']
		coordinates['longitude'] = response[u'longitude']

	# Checking for valid Country-Code
	if response[u'country_code'] is None:
		coordinates['country_code'] = None
	else:
		coordinates['country_code'] = response[u'country_code']

	# Return coordinate hash
	return coordinates

# Function will deploy messages, it only stores the last message-recipient in the directory
def send_messages(param_messages):

	# Opening SMTP connection to POSTFIX server
	postfix_connection = mail.get_connection()
	postfix_connection.open()

	built_messages = []

	for message in param_messages:

		alt_msg = mail.EmailMultiAlternatives(
											message['subject'],
											message['plaintext_content'],
											message['from'],
											[ message['to'] ],
											connection=postfix_connection,
										)

		alt_msg.attach_alternative(message['html_content'], "text/html")

		built_messages.append(alt_msg)

	postfix_connection.send_messages(built_messages)

	postfix_connection.close()

def send_invitations(param_messages):
	for message in param_messages:
		file_name = (time.strftime("%d_%m_%Y_i") + str(message['pk']) + ".msg")
		command = 'mail -a "Content-type: multipart/mixed; boundary=\"mess_bound\"" -a "MIME-Version: 1.0" -s "{0}" {1} < /home/kgluce/mailprime/mailprime/invitations/{2}'.format(message['subject'], message['to'], file_name)

		f = open(('/home/kgluce/mailprime/mailprime/invitations/{0}'.format(file_name)), 'w+')
		f.write(message['message'])
		f.close()

		os.system(command)
