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