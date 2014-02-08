from django.shortcuts import render
from django.template import RequestContext
from django.contrib.auth.models import User

def index(request):
	data = { "page_title": "Mailpri.me"}
	return render( request, 'index.html', data)

def login(request):
	data = { "page_title": "login" }
	csrfContext = RequestContext(request, data)
	return render(request, 'login.html', csrfContext)

def logout(request):
	data = { "page_title": "logout" }
	return render(request, 'index.html', data)
