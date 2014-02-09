from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from mailer.lib import authenticate_user
from django.http import HttpResponseRedirect

def index(request):
	data = { "page_title": "Mailpri.me"}
	return render( request, 'index.html', data)

def login(request):
	data = { "page_title": "login" }
	csrfContext = RequestContext(request, data)

	if request.method == 'POST':
		if authenticate_user(request, request.POST['username'], request.POST['password']):
			return HttpResponseRedirect('/')
		else:
			return HttpResponseRedirect('/login')
	else:
		return render(request, 'login.html', csrfContext)

def logout(request):
	data = { "page_title": "logout" }
	return render(request, 'index.html', data)
