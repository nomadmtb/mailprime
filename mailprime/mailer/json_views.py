from mailer.models import Profile, Campaign, Recipient, Event, Message
from mailer.lib import current_user
from collections import Counter
from django.http import HttpResponse
import json

def get_message_region_data(request, param_username, param_campaign_pk, param_message_pk):

	if current_user(request) and request.user.username == param_username:

		# Pre-build data, See Google Format -> https://developers.google.com/chart/interactive/docs/gallery/geochart
		data = []

		# Getting values for all of the associated read_events
		#country_data = Event.objects.values_list('country_code')

		read_events = Event.objects.filter( message__pk=param_message_pk,
											 message__campaign__pk=param_campaign_pk,
											 message__campaign__user__username=param_username )

		if read_events is None:
			raise Http404

		country_data = read_events.values_list('country_code')

		counter_data = Counter(item[0] for item in country_data)

		for k, v in counter_data.iteritems():
			entry = [ k, v ]
			data.append(entry)

		title = ['Region', 'Read Events']
		data = [title] + data

		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		raise Http404