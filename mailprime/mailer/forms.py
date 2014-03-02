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

class ProfileForm(forms.ModelForm):
	class Meta:
		model = Profile
		fields = ['public_email', 'time_zone']