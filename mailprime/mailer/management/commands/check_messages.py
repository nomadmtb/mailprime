from django.core.management.base import BaseCommand, CommandError
from datetime import datetime
from mailer import models
from mailer import lib

class Command(BaseCommand):
	help = 'Deploy campaign messages if the deploy dates are correct. Use with cron.'

	def handle(self, *args, **options):

		# Getting system time, and parsing out specific attributes.
		current_datetime = datetime.now()

		month_now = current_datetime.month
		day_now = current_datetime.day
		year_now = current_datetime.year
		hour_now = current_datetime.hour

		# Array will hold all of the message objects that we need to send out.
		# Query the database for the appropriate message objects.
		messages_to_deploy = models.Message.objects.filter(deployed=False,
													 	   deploy_date__month=month_now,
													       deploy_date__day=day_now,
													       deploy_date__year=year_now,
													       deploy_date__hour=hour_now,)

		# Okay, now we need to iterate through the messages and deploye them.
		for message in messages_to_deploy:

			# Calling lib function to send messages.
			lib.send_mail(message.build_messages())

			# Update message to show that it was deployed.
			message.deployed = True
			message.save()

			# Creating a send_event to show that it was sent with the 'cron' option.
			models.Send_Event(method="cron", message=message).save()