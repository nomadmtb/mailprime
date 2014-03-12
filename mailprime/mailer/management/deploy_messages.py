from django.core.management.base import BaseCommand, CommandError
from mailer import models
from mailer import lib

class Command(BaseCommand):
	args = '<message_id>'

	help = 'Deploy emails for a particular message object'

	def handle(self, *args, **options):

		try:
			mess = models.Message.objects.get(pk=int(message_id))
		except models.Message.DoesNotExist:
			raise CommandError('Message Does Not Exist, Try Again.')

		lib.send_messages(mess.build_messages())

		mess.deployed = True
		mess.save()

		self.stdout.write('Successfully Deployed Messages.')