import pytz
from django.utils import timezone
from mailer.models import Profile

class TZMiddleWare(object):

	def process_request(self, request):
		if request.user.is_authenticated():
			user_tz = request.session.get('user_timezone')

			if user_tz:
				timezone.activate(pytz.timezone(user_tz))
				#print "{0} Time-Zone: {1}".format(request.user.username,user_tz)
			else:
				pass
				profile_tz = request.user.profile.time_zone
				timezone.deactivate()
				timezone.activate(pytz.timezone(profile_tz))
				request.session['user_timezone'] = profile_tz
		else:

			timezone.deactivate()
