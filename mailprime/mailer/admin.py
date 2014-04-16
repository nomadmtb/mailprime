from django.contrib import admin
from mailer.models import Profile, Campaign, Recipient, Template, Event, Message, System_Template, Send_Event

# Register your models here.
admin.site.register(Profile)
admin.site.register(Campaign)
admin.site.register(Recipient)
admin.site.register(Template)
admin.site.register(Event)
admin.site.register(Message)
admin.site.register(System_Template)
admin.site.register(Send_Event)