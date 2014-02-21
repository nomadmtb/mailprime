from django.forms import ModelForm
from mailer.models import Campaign

# Model Forms for the Application

class CampaignForm(ModelForm):
	class Meta:
		model = Campaign
		fields = ['title', 'about']