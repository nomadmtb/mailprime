from django import forms
from mailer.models import Campaign, Message, Profile

# Model Forms for the Application

class CampaignForm(forms.ModelForm):
	class Meta:
		model = Campaign
		fields = ['title', 'about']
		widgets = { 'about': forms.Textarea(attrs={'cols': 35, 'rows': 6})}

class MessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['title', 'body', 'template', 'deploy_date']

class LoginForm(forms.Form):
	username = forms.CharField(max_length=50)
	password = forms.CharField(max_length=50, widget=forms.PasswordInput)

class UserProfileForm(forms.Form):
	public_email = forms.EmailField(max_length=254, label='Public Email Address')
	agree_terms = forms.BooleanField(initial=False, label='Agree Terms')
	time_zone = forms.ChoiceField(choices=Profile.TIME_ZONES, initial=0, label='Time Zone ( UTC Offset )')
	username = forms.CharField(max_length=50, label='Username')
	password = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Password')
	password_confirm = forms.CharField(max_length=150, widget=forms.PasswordInput, label='Password Confirm')
	email = forms.EmailField(max_length=254, label='Account Email Address')
