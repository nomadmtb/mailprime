from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.models import User

def index(request):
	return render_to_response('index.html',	{	"page_title": "Mailpri.me"	})

def login(request):
	return render_to_response('login.html',  {	"page_title": "Login"	})