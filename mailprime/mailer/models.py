from django.conf import settings
import hashlib
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import string
import re

# Create your models here.

class Profile(models.Model):
	"""This is the class that extends the User Class"""

	TIME_ZONES = (
		(-11, 'UTC -11:00'),
		(-10, 'UTC -10:00'),
		(-9, 'UTC -09:00'),
		(-8, 'UTC -08:00'),
		(-7, 'UTC -07:00'),
		(-6, 'UTC -06:00'),
		(-5, 'UTC -05:00'),
		(-4, 'UTC -04:00'),
		(-3, 'UTC -03:00'),
		(-2, 'UTC -02:00'),
		(-1, 'UTC -01:00'),
		(0, 'UTC 00:00'),
		(1, 'UTC +01:00'),
		(2, 'UTC +02:00'),
		(3, 'UTC +03:00'),
		(4, 'UTC +04:00'),
		(5, 'UTC +05:00'),
		(6, 'UTC +06:00'),
		(7, 'UTC +07:00'),
		(8, 'UTC +08:00'),
		(9, 'UTC +09:00'),
		(10, 'UTC +10:00'),
		(11, 'UTC +11:00'),
		(12, 'UTC +12:00'),
	)

	public_email = models.EmailField(max_length=254)
	agree_terms = models.BooleanField(default=False)
	time_zone = models.IntegerField(choices=TIME_ZONES, default=0, blank=False)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.public_email

class Campaign(models.Model):
	"""This is the campaign class that describes an indivual devivery event"""
	title = models.CharField(max_length=200)
	about = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True, blank=True)
	updated_date = models.DateTimeField(auto_now=True)
	active = models.BooleanField(default=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.title

	def link(self):
		return '/home/' + str(self.pk)

class Message(models.Model):
	"""This class holds the settings and content for the HTML templates"""

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

	title = models.CharField(max_length=200)
	body = models.TextField()
	link = models.URLField(max_length=200)
	template = models.ForeignKey('Template')
	campaign = models.ForeignKey('Campaign')
	deployed = models.BooleanField(default=False, blank=True)
	created_date = models.DateTimeField(auto_now_add=True)
	deploy_date = models.DateField()
	deploy_hour = models.IntegerField(choices=DEPLOY_HOURS, default=0, blank=False)
	message_id = models.CharField(max_length=200, blank=True)

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.message_id = hashlib.sha1(str(datetime.now()) + self.title + settings.MESSAGE_SALT).hexdigest()
		super(Message, self).save(*args, **kwargs)

	def build_messages(self):
		messages = []
		seleted_campaign = self.campaign
		recipients = Recipient.objects.filter(campaign=seleted_campaign, active=True)
		selected_template = self.template

		for recipient in recipients:
			built_template = string.replace(selected_template.content, "{{ campaign_title }}", seleted_campaign.title)
			built_template = string.replace(built_template, "{{ title }}", self.title)
			built_template = string.replace(built_template, "{{ owner_email }}", seleted_campaign.user.email)
			built_template = string.replace(built_template, "{{ recipient_email }}", recipient.email)
			built_template = string.replace(built_template, "{{ body }}", self.body)
			built_template = string.replace(built_template, "{{ link }}", self.link)
			built_template = string.replace(built_template, "{{ date_today }}", datetime.now().strftime('%Y-%m-%d %H:%M'))
			track_url = "http://127.0.0.1/tracker/visit/{0}/{1}.jpg".format(recipient.tracking_id, self.message_id)
			built_template = string.replace(built_template, "{{ tracking_link }}", track_url)
			built_template = re.sub('[\t]', '', str(built_template))
			message = {'to': str(recipient.email), 'from': str(seleted_campaign.user.email), 'subject': str(self.title), 'message': built_template}
			messages.append(message)

		return messages

	def __unicode__(self):
		return self.title


class Recipient(models.Model):
	"""This is the class that will hold contact information"""
	email = models.EmailField(max_length=254)
	created_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)
	invited = models.BooleanField(default=False)
	tracking_id = models.CharField(max_length=200, blank=True)
	campaign = models.ForeignKey('Campaign')

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.tracking_id = hashlib.sha1(str(datetime.now()) + self.email + settings.RECIPIENT_SALT).hexdigest()
		super(Recipient, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.email

class Event(models.Model):
	"""This is the class that will hold 'read' events for a recipient"""
	ip_address = models.GenericIPAddressField(protocol='IPv4')
	latitude = models.FloatField()
	longitude = models.FloatField()
	created_date = models.DateTimeField(auto_now_add=True)
	recipient = models.ForeignKey('Recipient')
	message = models.ForeignKey('Message')

	def __unicode__(self):
		return self.ip_address

class Template(models.Model):
	"""This is the class that will hold the different HTML template data for the messages"""
	title = models.CharField(max_length=200)
	content = models.TextField()

	def __unicode__(self):
		return self.title

class System_Template(models.Model):
	"""This is the class that will hold the templates that are used by the system, internal only"""
	title = models.CharField(max_length=200)
	content = models.TextField()

	def __unicode__(self):
		return self.title