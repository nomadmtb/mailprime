from django.contrib import admin
from mailer.models import Profile, Campaign, Recipient

# Register your models here.
admin.site.register(Profile)
admin.site.register(Campaign)
admin.site.register(Recipient)