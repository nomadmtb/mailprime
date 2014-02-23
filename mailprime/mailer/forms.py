from django.forms import ModelForm, Textarea
from mailer.models import Campaign, Message

# Model Forms for the Application

class CampaignForm(ModelForm):
	class Meta:
		model = Campaign
		fields = ['title', 'about']
		widgets = { 'about': Textarea(attrs={'cols': 35, 'rows': 6})}

class MessageForm(ModelForm):
	class Meta:
		model = Message
		fields = ['title', 'body', 'template', 'deploy_date']