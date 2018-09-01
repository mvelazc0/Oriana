# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

class User(models.Model):

    username = models.CharField(max_length=200)

    ## Authentication Statistics
    succ_auth_events = models.IntegerField(default=0)
    failed_auth_events = models.IntegerField(default=0)

    unique_succ_local_hosts = models.IntegerField(default=0)
    unique_succ_remote_hosts= models.IntegerField(default=0)

    unique_failed_remote_hosts = models.IntegerField(default=0)

    unique_succ_rdp_hosts = models.IntegerField(default=0)
    unique_succ_network_hosts = models.IntegerField(default=0)

    def __str__(self):
        return self.username

class Host(models.Model):

    hostname = models.CharField(max_length=200)

    ## Host Statistics
    total_succ_auths = models.IntegerField(default=0)
    total_failed_auths = models.IntegerField(default=0)

    unique_succ_remote_users = models.IntegerField(default=0)
    unique_succ_local_users = models.IntegerField(default=0)

    unique_failed_remote_users = models.IntegerField(default=0)
    unique_failed_local_users = models.IntegerField(default=0)

    def __str__(self):
        return self.hostname

class SourceIp(models.Model):

    #sourceip = models.GenericIPAddressField(blank=True,null=True)
    sourceip = models.CharField(max_length=100, blank=True)
    hostname = models.CharField(max_length=100, blank=True)

    total_succ_auths = models.IntegerField(default=0)
    total_failed_auths=models.IntegerField(default=0)

    unique_succ_remote_hosts = models.IntegerField(default=0)
    unique_failed_remote_hosts = models.IntegerField(default=0)

    def __str__(self):
        return str(self.sourceip) + ":"+str(self.hostname)

class Service(models.Model):

    servicename = models.CharField(max_length=1000)
    imagepath = models.CharField(max_length=10000)
    servicetype = models.CharField(max_length=30)

    count = models.IntegerField(default=0)
    ngramscore = models.IntegerField(default=0)

    def __str__(self):
        return self.servicename

class Task(models.Model):

    taskname = models.CharField(max_length=1000)
    imagepath = models.CharField(max_length=10000)
    arguments = models.CharField(max_length=10000)

    count = models.IntegerField(default=0)
    ngramscore = models.IntegerField(default=0)

    def __str__(self):
        return self.taskname

class FA_imagepath(models.Model):

    imagepath = models.CharField(max_length=10000)
    count = models.IntegerField(default=0)
    characterscount = models.IntegerField(default=0)


class Event_4624(models.Model):

    time= models.DateTimeField()
    host= models.ForeignKey(Host, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=200)
    logontype = models.CharField(max_length=200)
    sourcehost = models.CharField(max_length=200)
    processname = models.CharField(max_length=5000)
    status = models.CharField(max_length=200)

    #sourceip = models.CharField(max_length=200)
    sourceip = models.ForeignKey(SourceIp,null=True)

class Event_4625(models.Model):

    time= models.DateTimeField()
    host= models.ForeignKey(Host, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    domain = models.CharField(max_length=200)
    logontype = models.CharField(max_length=200)
    sourcehost = models.CharField(max_length=200)
    processname = models.CharField(max_length=5000)

    status = models.CharField(max_length=200)
    substatus = models.CharField(max_length=200)

    #sourceip = models.CharField(max_length=200)
    sourceip = models.ForeignKey(SourceIp, null=True)

class Event_4776(models.Model):

    time= models.DateTimeField()
    host= models.ForeignKey(Host, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    procname = models.CharField(max_length=500)
    status = models.CharField(max_length=200)

class Event_4672(models.Model):

    time= models.DateTimeField()
    host= models.ForeignKey(Host, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    privilegelist= models.CharField(max_length=1500)

class Event_4688(models.Model):

    time= models.DateTimeField()
    host= models.ForeignKey(Host, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.CharField(max_length=200)

class Event_7045(models.Model):

    time = models.DateTimeField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    service= models.ForeignKey(Service, on_delete=models.CASCADE)


    def __str__(self):
        return self.host.hostname + ":"+self.service.servicename

class Event_5140(models.Model):

    time = models.DateTimeField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    sourceip = models.ForeignKey(SourceIp, null=True)
    sharename = models.CharField(max_length=100)

    def __str__(self):
        return self.sharename

class Event_4698(models.Model):

    time = models.DateTimeField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    def __str__(self):
        return str(self.host) + ":"+str(self.task.taskname)

class WmiEvent_2(models.Model):

    time = models.DateTimeField()
    host = models.ForeignKey(Host, on_delete=models.CASCADE)
    operationid= models.CharField(max_length=100)
    operation = models.CharField(max_length=1000)

class PossibleLmSession(models.Model):

    start = models.DateTimeField()
    end= models.DateTimeField()
    delta= models.CharField(max_length=50,null=True)
    hosts= models.CharField(max_length=3,null=True)
    users= models.CharField(max_length=3,null=True)

    # list of users involved in the campaign
    # used services and image paths
    # show unique services and binaries used
    # need to know what the source is

class PossibleLM(models.Model):


    auth= models.ForeignKey(Event_4624, on_delete=models.CASCADE)
    event_7045 = models.ForeignKey(Event_7045, on_delete=models.CASCADE, null=True)
    event_4698 = models.ForeignKey(Event_4698, on_delete=models.CASCADE, null=True)
    event_wmi_2 = models.ForeignKey(WmiEvent_2, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=200)

    attack_progression= models.ForeignKey(PossibleLmSession, related_name='attacks', on_delete=models.CASCADE, null=True, default=None)

class SuspiciousUserBehavior(models.Model):

    name = models.CharField(max_length=200)
    description= models.CharField(max_length=2000)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

class SuspiciousSourceBehavior(models.Model):

    name = models.CharField(max_length=200)
    description= models.CharField(max_length=2000)
    source = models.ForeignKey(SourceIp, on_delete=models.CASCADE)
    start = models.DateTimeField()
    end = models.DateTimeField()

