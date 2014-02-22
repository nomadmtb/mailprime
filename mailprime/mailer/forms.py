from django.forms import ModelForm
from mailer.models import Campaign, Message

# Model Forms for the Application

class CampaignForm(ModelForm):
	class Meta:
		model = Campaign
		fields = ['title', 'about']

class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ['title', 'body', 'template', 'deploy_date']