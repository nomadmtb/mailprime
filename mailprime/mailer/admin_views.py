from django.shortcuts import render
from django.template import RequestContext
from mailer.lib import authenticate_user, current_user, current_staff, logout_user, geo_locate, generate_form_errors
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.contrib import messages


# Index page for administrative area.
def index(request):

	# If current user is authenticated and it staff.
	if current_staff(request):

		page_vars = {"page_title": 'Administrative Interface'}

		return render(request, 'administrative/index.html', page_vars)

	else:
		raise Http404