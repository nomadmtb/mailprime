from django.conf import settings
import hashlib
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
import string
import re
import pytz

# Create your models here.

class Profile(models.Model):
	"""This is the class that extends the User Class"""

	TIME_ZONES = [(x,x) for x in pytz.common_timezones]

	agree_terms = models.BooleanField(default=False)
	time_zone = models.CharField(choices=TIME_ZONES, default="UTC", blank=False, max_length=50)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.user.email

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

	def build_invitations(self):

		# Empty array that will contain messages
		messages = []
		recipients = Recipient.objects.filter(campaign=self.pk, invited=False, active=False)
		selected_template = System_Template.objects.get(title='campaign_invitation')

		for recipient in recipients:
			built_template = string.replace( selected_template.content, "{{ campaign_title }}", self.title )
			built_template = string.replace( built_template, "{{ title }}", 'MailPrime Campaign Invitation' )
			built_template = string.replace( built_template, "{{ owner_email }}", self.user.email )
			built_template = string.replace( built_template, "{{ recipient_email }}", recipient.email )

			accept_link = "http://nomadmtb.com:8000/tracker/auth/{0}".format( recipient.tracking_id )
			built_template = string.replace( built_template, "{{ accept_link }}", accept_link )

			deny_link = "http://nomadmtb.com:8000/tracker/unsub/{0}".format( recipient.tracking_id )
			built_template = string.replace( built_template, "{{ deny_link }}", deny_link )

			built_template = string.replace( built_template, "{{ about }}", self.about )

			built_template = re.sub('[\t]', '', built_template.encode('utf-8'))

			message = {
						'to': recipient.email.encode('utf-8'),
						'from': self.user.email.encode('utf-8'),
						'subject': self.title.encode('utf-8'),
						'message': built_template,
						'pk': self.pk,
						}
			messages.append(message)

		return messages


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
	unsub_count = models.IntegerField(default=0)

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.message_id = hashlib.sha1(str(datetime.now()) + self.title + settings.MESSAGE_SALT).hexdigest()
		super(Message, self).save(*args, **kwargs)

	def build_sample(self):
		message = ''
		selected_campaign = self.campaign
		selected_template = self.template

		# Construct sample message
		built_template = string.replace(selected_template.content, "{{ campaign_title }}", selected_campaign.title)
		built_template = string.replace(built_template, "{{ tracking_link }}", "")
		built_template = string.replace(built_template, "{{ unsub_link }}", "")
		built_template = string.replace(built_template, "{{ title }}", self.title)
		built_template = string.replace(built_template, "{{ owner_email }}", selected_campaign.user.email)
		built_template = string.replace(built_template, "{{ recipient_email }}", "sample@mailpri.me")
		built_template = string.replace(built_template, "{{ body }}", self.body)
		built_template = string.replace(built_template, "{{ link }}", self.link)

		# Searching for HTML in email template, ommiting weird message-boundaries
		substring = built_template[built_template.find('<html'):built_template.find('</html>')+len('</html>')]

		substring = string.replace(substring, '\t', '')
		substring = string.replace(substring, '\r', '')
		substring = string.replace(substring, '\n', '')

		# Return HTML
		return substring

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
			track_url = "http://nomadmtb.com:8000/tracker/visit/{0}/{1}.jpg".format(recipient.tracking_id, self.message_id)
			built_template = string.replace(built_template, "{{ tracking_link }}", track_url)
			unsub_url = "http://nomadmtb.com:8000/tracker/unsub/{0}".format(recipient.tracking_id)
			built_template = string.replace(built_template, "{{ unsub_link }}", unsub_url)
			built_template = re.sub('[\t]', '', built_template.encode('utf-8'))
			message = {'to': recipient.email.encode('utf-8'), 'from': seleted_campaign.user.email.encode('utf-8'), 'subject': self.title.encode('utf-8'), 'message': built_template, 'pk': self.pk}
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

	# Unique constraint between email, and campaign
	class Meta:
		unique_together = ('email', 'campaign')

	# Save method overwritten, it will generate tracking_id when created
	def save(self, *args, **kwargs):
		if self.pk is None:
			self.tracking_id = hashlib.sha1(str(datetime.now()) + self.email + settings.RECIPIENT_SALT).hexdigest()
		super(Recipient, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.email

class Event(models.Model):
	"""This is the class that will hold 'read' events for a recipient"""
	ip_address = models.GenericIPAddressField(protocol='IPv4')
	country_code = models.CharField(max_length=100)
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
