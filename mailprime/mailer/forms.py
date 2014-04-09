from django import forms
from mailer.models import Campaign, Message, Profile, Template, Recipient
from django.contrib.auth.models import User
import pdb
import re
from datetime import datetime, timedelta
import pytz

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

	DEPLOY_HOURS = (
		(0, '12:00 AM'),
		(1, '1:00 AM'),
		(2, '2:00 AM'),
		(3, '3:00 AM'),
		(4, '4:00 AM'),
		(5, '5:00 AM'),
		(6, '6:00 AM'),
		(7, '7:00 AM'),
		(8, '8:00 AM'),
		(9, '9:00 AM'),
		(10, '10:00 AM'),
		(11, '11:00 AM'),
		(12, '12:00 PM'),
		(13, '1:00 PM'),
		(14, '2:00 PM'),
		(15, '3:00 PM'),
		(16, '4:00 PM'),
		(17, '5:00 PM'),
		(18, '6:00 PM'),
		(19, '7:00 PM'),
		(20, '8:00 PM'),
		(21, '9:00 PM'),
		(22, '10:00 PM'),
		(23, '11:00 PM'),
		)

	temp_deploy_hour = forms.ChoiceField(choices=DEPLOY_HOURS, initial=0)
	user_timezone = forms.CharField(widget=forms.HiddenInput())

	class Meta:
		model = Message
		fields = ['title', 'body', 'link', 'template', 'deploy_date']
		localized_fields = ['__all__']

	def clean(self):
		cleaned_data = self.cleaned_data
		deploy_hour = cleaned_data['temp_deploy_hour']
		user_timezone = cleaned_data['user_timezone']

		### USE LOCALIZE, NOT REPLACE. REPLACE DOESN'T TAKE INTO ACCOUNT DST ###

		print "Timezone: {0}".format(cleaned_data['deploy_date'].strftime('%Z'))

		if earliest_time > desired_time:
			raise forms.ValidationError("Deploy date must be at least 3 hours into the future")

		print cleaned_data

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
					raise forms.ValidationError("Password: Passwords must be letters and numbers, and between 8 and 50 characters")


		if email == '':
			raise forms.ValidationError("Email: Required Field")

		return cleaned_data

class ContactUploadForm(forms.Form):

	contact_file = forms.FileField()
