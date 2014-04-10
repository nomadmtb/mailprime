from django.core.management.base import BaseCommand, CommandError
from mailer import models
from mailer import lib

class Command(BaseCommand):
	args = '<campaign_id campaign_id...>'

	help = 'Deploy campaign invitations for a particular campaign object'

	def handle(self, *args, **options):
		cam = None

		for campaign in args:
			try:
				cam = models.Campaign.objects.get(pk=int(campaign))
			except models.Message.DoesNotExist:
				raise CommandError('Campaign Does Not Exist, Try Again.')

			lib.send_mail(cam.build_invitations())
			self.stdout.write('Successfully Deployed Invitations.')

		# Update recipients with invited status
		models.Recipient.objects.filter(campaign=cam).update(invited=True)