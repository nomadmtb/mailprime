from django import forms
from mailer.models import Campaign, Message, Profile, Template, Recipient
import pdb
import re
from django.contrib.auth.models import User
from datetime import datetime

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
	deploy_date = forms.DateField(label='Deploy Date')
	class Meta:
		model = Message
		fields = ['title', 'body', 'link', 'template', 'deploy_date', 'deploy_hour']

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
		username = cleaned_data.get("username")
		password = cleaned_data.get("password")
		password_confirm = cleaned_data.get("password_confirm")
		email = cleaned_data.get("email")

		print agree_terms

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
