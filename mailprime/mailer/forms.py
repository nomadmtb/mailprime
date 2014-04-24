from django import forms
from mailer.models import Campaign, Message, Profile, Template, Recipient
from django.contrib.auth.models import User
import pdb
import re
from datetime import datetime, timedelta
import pytz
import magic

# Model Forms for the Application

class CampaignForm(forms.ModelForm):
	class Meta:
		model = Campaign
		fields = ['title', 'about']
		widgets = { 'about': forms.Textarea(attrs={'cols': 35, 'rows': 6})}

class RecipientForm(forms.ModelForm):
	class Meta:
		model = Recipient
		fields = ['email']

class MessageForm(forms.ModelForm):

	# Overriding this field so we can format the output with no time
	deploy_date = forms.DateTimeField(widget=forms.DateInput(format='%Y-%m-%d'))

	class Meta:
		model = Message
		fields = ['title', 'body', 'link', 'template', 'deploy_date', 'deploy_hour']
		localized_fields = ['__all__']

	def clean(self):
		cleaned_data = self.cleaned_data
		deploy_hour = int(cleaned_data['deploy_hour'])

		# Apply deploy-hour to deploy-date
		cleaned_data['deploy_date'] = cleaned_data['deploy_date'].replace(hour=deploy_hour, minute=0)

		# Converting both times to UTC
		deploy_utc = cleaned_data['deploy_date'].astimezone(pytz.utc)
		system_utc = datetime.now(pytz.utc)
		earliest_utc = system_utc + timedelta(hours=3)

		print "DEPLOY UTC -> {0}".format(deploy_utc)
		print "SYSTEM UTC -> {0}".format(system_utc)
		print "EARLIEST UTC -> {0}".format(earliest_utc)


		# Make sure deploy date is at least 3 hrs into the future
		if deploy_utc < earliest_utc:
			raise forms.ValidationError("ERROR: Deploy Date Must Be At Least 3 Hours Into The Future")

		else:
			# Overwrite cleaned_data['deploy_date'] with validated datetime
			cleaned_data['deploy_date'] = deploy_utc

		return cleaned_data

class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class UserProfileForm(forms.Form):
	agree_terms = forms.BooleanField(initial=False, label='Agree Terms', required=False)
	time_zone = forms.ChoiceField(choices=Profile.TIME_ZONES, initial=0, label='Time Zone', required=False)
	password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Password', required=False)
	password_confirm = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Password Confirm', required=False)
	email = forms.EmailField(max_length=254, label='Account Email Address', required=False)

	def clean(self):
		cleaned_data = self.cleaned_data

		agree_terms = cleaned_data.get("agree_terms")
		time_zone = cleaned_data.get("time_zone")
		password = cleaned_data.get("password")
		password_confirm = cleaned_data.get("password_confirm")
		email = cleaned_data.get("email")

		if agree_terms == False:
			raise forms.ValidationError("Agree Terms: You Must Agree To Our Terms Of Service")

		if password != '' and password_confirm != '':
			if password_confirm != password:
				raise forms.ValidationError("Password: Passwords Must Match")
			else:
				pattern = re.compile('^[A-Za-z0-9]{8,50}$')
				if pattern.match(password) is None:
					raise forms.ValidationError("Password: Passwords can only be [A-Z, a-z, 0-9] with a minimum length of 8.")


		if email == '':
			raise forms.ValidationError("Email: Required Field")

		return cleaned_data

class ContactUploadForm(forms.Form):

	contact_file = forms.FileField(required=True)

	def clean(self):
		cleaned_data = self.cleaned_data

		# Open file and read some of the data
		uploaded_file = cleaned_data.get('contact_file')
		sample_buffer = uploaded_file.read(1500)

		# Use that buffer to determine mime-type with magic
		file_mime = magic.from_buffer(sample_buffer, mime=True)

		# Parse mime type to get filetype.
		# Ex: 'text/plain; charset=us-ascii --->>> 'text/plain' 
		file_type = file_mime.split(';')[0]

		# File_type should be 'text/plain'
		if file_type != 'text/plain':
			raise forms.ValidationError("File Validation Failed. Plain text-files only.")

		# File_type is correct, return the cleaned data	
		else:

			return cleaned_data

class AdminMessageForm(forms.ModelForm):

	# Overriding this field so we can format the output with no time
	deploy_date = forms.DateTimeField(widget=forms.DateInput(format='%Y-%m-%d'))

	class Meta:
		model = Message
		fields = ['title', 'body', 'link', 'template', 'deployed', 'deploy_date', 'deploy_hour']
		localized_fields = ['__all__']

	def clean(self):
		cleaned_data = self.cleaned_data
		deploy_hour = int(cleaned_data['deploy_hour'])

		# Apply deploy-hour to deploy-date
		cleaned_data['deploy_date'] = cleaned_data['deploy_date'].replace(hour=deploy_hour, minute=0)

		# Converting both times to UTC
		deploy_utc = cleaned_data['deploy_date'].astimezone(pytz.utc)

		# Overwrite cleaned_data['deploy_date'] with datetime.
		cleaned_data['deploy_date'] = deploy_utc

		return cleaned_data

class AdminCampaignForm(forms.ModelForm):

	class Meta:
		model = Campaign
		fields = ['title', 'about', 'active', 'unsub_count']
		widgets = { 'about': forms.Textarea(attrs={'cols': 35, 'rows': 6})}

