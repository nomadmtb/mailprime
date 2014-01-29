from django.conf import settings
import hashlib
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	"""This is the class that extends the User Class"""
	public_email = models.EmailField(max_length=254)
	agree_terms = models.BooleanField(default=False)
	user = models.OneToOneField(User)

	def __unicode__(self):
		return self.public_email

class Campaign(models.Model):
	"""This is the campaign class that describes an indivual devivery event"""
	title = models.CharField(max_length=200)
	about = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

	def __unicode__(self):
		return self.title

class Recipient(models.Model):
	"""This is the class that will hold contact information"""
	email = models.EmailField(max_length=254)
	created_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)
	tracking_id = models.CharField(max_length=200)
	campaign = models.ForeignKey('Campaign')

	def save(self, *args, **kwargs):
		if self.pk is None:
			self.tracking_id = hashlib.sha1(str(datetime.now()) + settings.RECIPIENT_SALT).hexdigest()
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

	def __unicode__(self):
		return self.title
