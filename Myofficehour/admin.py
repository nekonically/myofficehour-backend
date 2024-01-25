from django.contrib import admin
from Myofficehour.models import Officehour,Location,Status,Participant

# Register your models here.
admin.site.register(Officehour)
admin.site.register(Location)
admin.site.register(Status)
admin.site.register(Participant)