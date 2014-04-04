from mailer.models import Profile, Campaign, Recipient, Event, Message
from mailer.lib import current_user
from collections import Counter
from django.http import HttpResponse
import datetime, pytz
import json

def get_message_region_data(request, param_username, param_campaign_pk, param_message_pk):

	if current_user(request) and request.user.username == param_username:

		# Pre-build data, See Google Format -> https://developers.google.com/chart/interactive/docs/gallery/geochart
		data = {}

		# Getting values for all of the associated read_events
		#country_data = Event.objects.values_list('country_code')

		read_events = Event.objects.filter( message__pk=param_message_pk,
											 message__campaign__pk=param_campaign_pk,
											 message__campaign__user__username=param_username )

		if read_events is None:
			return HttpResponse(json.dumps([]), content_type='application/json')

		# Load Region-data	
		region_data = []
		country_data = read_events.values_list('country_code')
		counter_data = Counter(item[0] for item in country_data)

		for k, v in counter_data.iteritems():
			entry = [ k, v ]
			region_data.append(entry)

		region_title = ['Region', 'Read Events']
		region_data = [region_title] + region_data
		data['region_data'] = region_data
		# End Region-data

		# Load Coordinate Data
		coordinate_data = []
		coord_data = read_events.values_list('latitude', 'longitude', 'recipient__email')

		for item in coord_data:
			entry = [ item[0], item[1], item[2] ]
			coordinate_data.append(entry)

		coord_title = ['Lat', 'Lon', 'Name']
		coordinate_data = [coord_title] + coordinate_data
		data['coordinate_data'] = coordinate_data
		# End Coordinate Data

		# Load Response Perc. Data
		response_data = []
		users_responded = read_events.values('recipient__email').distinct().count()

		num_users = Recipient.objects.filter( campaign__pk=param_campaign_pk,
											  campaign__user__username=param_username ).count()



		response_title = ['Status', 'Responce Rate']
		response_data.append(['Read', users_responded])
		response_data.append(['Not Read', (num_users - users_responded)])

		response_data = [response_title] + response_data
		data['response_data'] = response_data
		# End Response Perc. Data

		# Day of Week Data
		day_of_week_data = []
		weekly_data = []
		week_title = ['Weekday', 'Read Events']

		# Getting User Tz
		user_tz = pytz.timezone(
			Profile.objects.get( user=request.user).time_zone )

		event_week_data = read_events.values_list('created_date')

		# Convert all times to user_tz
		for event_date in event_week_data:
			local_time = event_date[0].replace(tzinfo=pytz.utc).astimezone(user_tz)
			weekly_data.append(local_time.strftime("%A"))

		# Count Data
		week_counter_data = Counter(weekly_data)

		# Loading Data into array
		for k, v in week_counter_data.iteritems():
			day_of_week_data += [[ k, v ]]

		day_of_week_data = [week_title] + day_of_week_data
		data['weekday_data'] = day_of_week_data
		# End Day of Week Data

		return HttpResponse(json.dumps(data), content_type='application/json')
	else:
		return HttpResponse('Unauthorized', status=401)

def get_sample_message(request, param_username, param_campaign_pk, param_message_pk):

	if current_user(request) and request.user.username == param_username:

		data = {}

		try:
			message = Message.objects.get(	pk=param_message_pk,
											campaign__pk=param_campaign_pk,
											campaign__user__username=param_username)
		except Message.DoesNotExist:

			return HttpResponse('Unauthorized', status=401)

		sample_message_html = message.build_sample()

		return HttpResponse(sample_message_html, content_type='text/html')

	else:
		return HttpResponse('Unauthorized', status=401)