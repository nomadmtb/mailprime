from django.shortcuts import render
from django.contrib.auth.models import User
from django.template import RequestContext
from mailer.lib import authenticate_user, current_user, current_staff, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages
from mailer.models import Send_Event


# Index page for administrative area.
def index(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'Administrative Interface'}

		# Getting recent send_events. Limit to 25 max.
		page_vars['send_events'] = Send_Event.objects.all().order_by('-send_date')[:25]

		# Getting recent users. Limit to 25 max.
		page_vars['users'] = User.objects.all().order_by('-last_login')[:25]

		return render(request, 'administrative/index.html', page_vars)

	else:
		raise Http404

def send_events(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'All Send Events'}

		page_vars['send_events'] = Send_Event.objects.all().order_by('-send_date')

		return render(request, 'administrative/send_events.html', page_vars)

	else:
		raise Http404

def users(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'All Users'}

		page_vars['users'] = User.objects.all().order_by('last_login')

		return render(request, 'administrative/users.html', page_vars)

	else:
		raise Http404
