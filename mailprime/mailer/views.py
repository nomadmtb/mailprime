from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

def index(request):
	data = { "page_title": "Mailpri.me"}
	return render( request, 'index.html', data)

def login(request):
	data = { "page_title": "login" }
	csrfContext = RequestContext(request, data)

	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username = username, password = password)

		# I should be using session data, and httpredirect, not render.		
		if user is not None:
			if user.is_active:
				auth_login(request,user)
				return render(request, 'index.html', { "notice": "Welcome "+username })
			else:
				return render(request, 'index.html', { "notice": "Your account is disabled" })
		else:
			return render(request, 'login.html', { "notice": "Login Failed" })

	return render(request, 'login.html', csrfContext)

def logout(request):
	data = { "page_title": "logout" }
	return render(request, 'index.html', data)
