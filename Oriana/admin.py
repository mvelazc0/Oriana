# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Host)
admin.site.register(Task)
admin.site.register(Service)
admin.site.register(Event_4624)
admin.site.register(Event_4625)
admin.site.register(Event_4776)
admin.site.register(Event_7045)
admin.site.register(Event_4698)
admin.site.register(WmiEvent_2)
admin.site.register(PossibleLM)
admin.site.register(PossibleLmSession)
admin.site.register(FA_imagepath)
admin.site.register(SuspiciousUserBehavior)
admin.site.register(SourceIp)
admin.site.register(SuspiciousSourceBehavior)
admin.site.register(Event_4672)
admin.site.register(Event_5140)

