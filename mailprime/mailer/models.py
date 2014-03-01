from django.conf import settings
import hashlib
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

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
	active = models.BooleanField(default=True)
	user = models.ForeignKey(User)

	def __unicode__(self):
		return self.title

	def link(self):
		return '/home/' + str(self.pk)

class Recipient(models.Model):
	"""This is the class that will hold contact information"""
	email = models.EmailField(max_length=254)
	created_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)
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

class Message(models.Model):
	"""This class holds the settings and content for the HTML templates"""
	title = models.CharField(max_length=200)
	body = models.TextField()
	template = models.ForeignKey('Template')
	campaign = models.ForeignKey('Campaign')
	created_date = models.DateTimeField(auto_now_add=True, blank=True)
	deploy_date = models.DateTimeField()
	message_id = models.CharField(max_length=200, blank=True)

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.message_id = hashlib.sha1(str(datetime.now()) + self.title + settings.MESSAGE_SALT).hexdigest()
		super(Message, self).save(*args, **kwargs)

	def __unicode__(self):
		return self.title
