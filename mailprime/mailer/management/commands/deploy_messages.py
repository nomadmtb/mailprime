from django.core.management.base import BaseCommand, CommandError
from mailer import models
from mailer import lib

class Command(BaseCommand):
	args = '<message_id message_id...>'

	help = 'Deploy emails for a particular message object'

	def handle(self, *args, **options):
		for message in args:
			try:
				mess = models.Message.objects.get(pk=int(message))
			except models.Message.DoesNotExist:
				raise CommandError('Message Does Not Exist, Try Again.')

			if mess.deployed:
				raise CommandError('ERROR: Message has already been deployed')
			else:
				lib.send_messages(mess.build_messages())
				self.stdout.write('Successfully Deployed Messages.')
				mess.deployed = True
				mess.save()
