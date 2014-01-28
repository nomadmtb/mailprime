from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	"""This is the class that extends the User Class"""
	public_email = models.EmailField(max_length=254)
	agree_terms = models.BooleanField(default=False)
	user = models.OneToOneField(User)

class Campaign(models.Model):
	"""This is the campaign class that describes an indivual devivery event"""
	title = models.CharField(max_length=200)
	about = models.TextField()
	created_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=True)

class Recipient(models.Model):
	"""This is the class that will hold contact information"""
	email = models.EmailField(max_length=254)
	created_date = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)
	tracking_id = models.CharField(max_length=200)
	campaign = models.ForeignKey('Campaign')

class Event(models.Model):
	"""This is the class that will hold 'read' events for a recipient"""
	ip_address = models.GenericIPAddressField(protocol='IPv4')
	latitude = models.FloatField()
	longitude = models.FloatField()
	created_date = models.DateTimeField(auto_now_add=True)
	recipient = models.ForeignKey('Recipient')

class Template(models.Model):
	"""This is the class that will hold the different HTML template data for the messages"""
	title = models.CharField(max_length=200)
	content = models.TextField()

class Message(models.Model):
	"""This class holds the settings and content for the HTML templates"""
	title = models.CharField(max_length=200)
	body = models.TextField()
	template = models.ForeignKey('Template')