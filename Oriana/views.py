# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.template import loader
from models import *
from django.db.models import Q
from django.db.models import Count
#from django.shortcuts import render


def hosts(request):

    t = loader.get_template('hosts.html')
    hosts=Host.objects.all()
    c = {'hosts': hosts}
    return HttpResponse(t.render(c, request), content_type='text/html')


def shosts(request):

    t = loader.get_template('shosts.html')
    shosts=SourceIp.objects.all()
    c = {'shosts': shosts}
    return HttpResponse(t.render(c, request), content_type='text/html')

def users(request):

    t = loader.get_template('users.html')
    users=User.objects.all().order_by('unique_succ_remote_hosts').reverse()
    c = {'users': users}
    return HttpResponse(t.render(c, request), content_type='text/html')

def services(request):

    t = loader.get_template('services.html')
    services=Service.objects.all()

    c = {'services': services}
    return HttpResponse(t.render(c, request), content_type='text/html')

def service(request, service_id):

    t = loader.get_template('service.html')
    service= Service.objects.get(id=service_id)
    events= Event_7045.objects.filter(service=service)

    c = {'service': service,'events':events}
    return HttpResponse(t.render(c, request), content_type='text/html')


def tasks(request):

    t = loader.get_template('tasks.html')
    tasks=Task.objects.all()
    c = {'tasks': tasks}
    return HttpResponse(t.render(c, request), content_type='text/html')

def task(request, task_id):

    t = loader.get_template('task.html')
    task= Task.objects.get(id=task_id)
    events= Event_4698.objects.filter(task=task)
    c = {'task': task,'events':events}
    return HttpResponse(t.render(c, request), content_type='text/html')

def dashboard(request):

    t = loader.get_template('dashboard.html')
    users=User.objects.count()
    hosts = Host.objects.count()
    services = Event_7045.objects.count()
    auths_suc = Event_4624.objects.count()
    auths_failed= Event_4625.objects.count()
    tasks= Event_4698.objects.count()
    wmis=WmiEvent_2.objects.count()

    uservices = Service.objects.count()
    utasks = Task.objects.count()

    possiblelms=PossibleLM.objects.count()
    possiblelm_service=PossibleLM.objects.filter(event_7045__isnull=False).count()
    possiblelm_task = PossibleLM.objects.filter(event_4698__isnull=False).count()
    possiblelm_wmi = PossibleLM.objects.filter(event_wmi_2__isnull=False).count()

    speciallogons = Event_4672.objects.count()
    fileshares = Event_5140.objects.count()
    localauths = Event_4776.objects.count()


    progressions=PossibleLmSession.objects.count()

    c = {'users': users,'hosts':hosts,'services':services,'auths':auths_suc + auths_failed,'wmis':wmis,'tasks':tasks,'uservices':uservices,'utasks':utasks,'possiblelms':possiblelms,'progressions':progressions,'possiblelm_service':possiblelm_service,'possiblelm_task':possiblelm_task,'possiblelm_wmi':possiblelm_wmi,'speciallogons':speciallogons,'fileshares':fileshares,'localauths':localauths}
    return HttpResponse(t.render(c, request), content_type='text/html')

def possible_lm(request):

    t = loader.get_template('possible_lm.html')
    events=PossibleLM.objects.all()
    c = {'events': events}
    return HttpResponse(t.render(c, request), content_type='text/html')


def possible_lm_detail(request, possiblelm_id):

    t = loader.get_template('possible_lm_detail.html')
    event=PossibleLM.objects.get(id=possiblelm_id)
    c = {'event': event, 'hosts': hosts}
    return HttpResponse(t.render(c, request), content_type='text/html')

def lm_sessions(request):

    t = loader.get_template('lm_sessions.html')
    progressions = PossibleLmSession.objects.all()
    deltas=[]
    for p in progressions:
        deltas.append(p.end-p.start)
    #print deltas
    c = {'progressions': progressions,'deltas':deltas}
    return HttpResponse(t.render(c, request), content_type='text/html')

def lmsession(request, lmsession_id):

    t = loader.get_template('lmsession.html')
    aprogression=PossibleLmSession.objects.get(id=lmsession_id)
    #print type(aprogression.attacks.all())
    events= aprogression.attacks.all().order_by('auth__time')
    c= {'aprogression': aprogression,'events': events}
    return HttpResponse(t.render(c, request), content_type='text/html')

def host(request, host_id):

    t = loader.get_template('host.html')
    host=Host.objects.get(id=host_id)
    auth_remote = Event_4624.objects.filter(host=host).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time')
    auth_local = Event_4624.objects.filter(host=host).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time')
    auth_remote_failed = Event_4625.objects.filter(host=host).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time')
    users_remote=[]
    users_local = []

    for ur in Event_4624.objects.filter(host=host).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('user').distinct():
        user=User.objects.get(id=ur['user'])
        users_remote.append(user)

    for ul in Event_4624.objects.filter(host=host).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('user').distinct():
        user=User.objects.get(id=ul['user'])
        users_local.append(user)

    c = {'host': host,'auth_remote':auth_remote,'auth_remote_failed':auth_remote_failed,'auth_local':auth_local,'users_remote':users_remote,'users_local':users_local}
    return HttpResponse(t.render(c, request), content_type='text/html')

def shost(request, shost_id):

    t = loader.get_template('shost.html')
    shost=SourceIp.objects.get(id=shost_id)
    auth_remote_succ = Event_4624.objects.filter(sourceip=shost).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time')
    auth_remote_failed = Event_4625.objects.filter(sourceip=shost).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time')
    #print str(len(auth_remote_succ))
    #print str(len(auth_remote_failed))
    users_remote=[]
    users_local = []
    """
    for ur in Event_4624.objects.filter(host=host).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('user').distinct():
        user=User.objects.get(id=ur['user'])
        users_remote.append(user)

    for ul in Event_4624.objects.filter(host=host).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('user').distinct():
        user=User.objects.get(id=ul['user'])
        users_local.append(user)
    """

    #c = {'host': host,'auth_remote_succ':auth_remote_succ,'auth_remote_failed':auth_remote_failed,'users_remote':users_remote,'users_local':users_local}
    c = {'host': host, 'auth_remote_succ': auth_remote_succ, 'auth_remote_failed': auth_remote_failed}
    return HttpResponse(t.render(c, request), content_type='text/html')



def user(request, user_id):

    t = loader.get_template('user.html')
    user = User.objects.get(id=user_id)
    auth_remote = Event_4624.objects.filter(user=user).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time')
    auth_local = Event_4624.objects.filter(user=user).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time')
    auth_failed = Event_4625.objects.filter(user=user).order_by('time')
    auth_local_user = Event_4776.objects.filter(user=user).order_by('time')
    hosts_remote=[]
    hosts_local = []
    for ar in Event_4624.objects.filter(user=user).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('host').distinct():
        host=Host.objects.get(id=ar['host'])
        hosts_remote.append(host)

    for al in Event_4624.objects.filter(user=user).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('host').distinct():
        host=Host.objects.get(id=al['host'])
        hosts_local.append(host)
    c = {'user': user, 'auth_remote':auth_remote,'auth_local':auth_local,'auth_events':'auth_events','hosts_remote':hosts_remote,'hosts_local':hosts_local,'auth_failed':auth_failed,'auth_local_user':auth_local_user}
    return HttpResponse(t.render(c, request), content_type='text/html')



def fa_cmdline(request):

    t = loader.get_template('fa_cmdline.html')
    cmdlines=FA_imagepath.objects.all()

    c = {'cmdlines': cmdlines}
    return HttpResponse(t.render(c, request), content_type='text/html')


def fa_cmdline_detail(request,cmdline_id):

    t = loader.get_template('fa_cmdline_detail.html')
    cmdline=FA_imagepath.objects.get(id=cmdline_id).imagepath

    services=Event_7045.objects.filter(service__imagepath=cmdline)
    tasks=Event_4698.objects.filter(task__imagepath=cmdline)
    c = {'services': services,'tasks':tasks}
    return HttpResponse(t.render(c, request), content_type='text/html')

def suspicious_behavior(request):

    t = loader.get_template('suspicious_behavior.html')
    types=["User: Privilege Enumeration","User: High number of destinations","User: Roaming Authentication","User: Local Account Usage","Source Host: Possible User Enumeration","Source Host: Possible Password Spray/Brute Force","Source Host: High number of users"]
    totals=[]
    for type in types:
        total=len(SuspiciousUserBehavior.objects.filter(name=type))
        if total >0:
            totals.append([type,total])

    for type in types:
        total=len(SuspiciousSourceBehavior.objects.filter(name=type))
        if total >0:
            totals.append([type,total])

    c = {'totals': totals}
    return HttpResponse(t.render(c, request), content_type='text/html')

def suspicious_behavior_type(request,type):
    #print type
    t = loader.get_template('suspicious_behavior_type.html')
    suspicious_user_behavior=SuspiciousUserBehavior.objects.filter(name=type)
    suspicious_host_behavior = SuspiciousSourceBehavior.objects.filter(name=type)
    #print len(suspicious_host_behavior)
    #print len(suspicious_user_behavior)
    c = {'suspicious_user_behavior': suspicious_user_behavior,"suspicious_host_behavior":suspicious_host_behavior}
    return HttpResponse(t.render(c, request), content_type='text/html')

def suspicious_user_behavior(request):

    t = loader.get_template('suspicious_user_behavior.html')
    users=User.objects.annotate(suspicious_count=Count('suspicioususerbehavior')).filter(suspicious_count__gt=0)

    c = {'users': users}
    return HttpResponse(t.render(c, request), content_type='text/html')

def suspicious_behavior_user(request,user_id):

    t = loader.get_template('suspicious_user_behavior_user.html')
    suspicious_behavior=SuspiciousUserBehavior.objects.filter(user_id=user_id)
    c = {'suspicious_behavior': suspicious_behavior}
    return HttpResponse(t.render(c, request), content_type='text/html')


def suspicious_user_behavior_detail(request,s_id):

    t = loader.get_template('suspicious_user_behavior_detail.html')
    suspicious_behavior=SuspiciousUserBehavior.objects.get(id=s_id)

    auth_succ_remote=Event_4624.objects.filter(user=suspicious_behavior.user).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).order_by('time')
    auth_failed_remote = Event_4625.objects.filter(user=suspicious_behavior.user).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).order_by('time')

    unique_hosts_succ_remote=Event_4624.objects.filter(user=suspicious_behavior.user).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).values('host').distinct()
    unique_hosts_failed_remote = Event_4625.objects.filter(user=suspicious_behavior.user).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).values('host').distinct()

    local_auths=Event_4624.objects.filter(user=suspicious_behavior.user).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).order_by('time')
    local_user_auths=Event_4776.objects.filter(user=suspicious_behavior.user).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end))

    unique_hosts=len(unique_hosts_failed_remote)+len(unique_hosts_succ_remote)

    c = {'suspicious_behavior': suspicious_behavior,'auth_failed_remote':auth_failed_remote,'auth_succ_remote':auth_succ_remote,'local_auths':local_auths,'local_user_auths':local_user_auths,'unique_hosts':unique_hosts}

    return HttpResponse(t.render(c, request), content_type='text/html')


def suspicious_source_behavior(request):

    t = loader.get_template('suspicious_source_behavior.html')
    sources=SourceIp.objects.annotate(suspicious_count=Count('suspicioussourcebehavior')).filter(suspicious_count__gt=0)

    c = {'sources': sources}
    return HttpResponse(t.render(c, request), content_type='text/html')

def suspicious_behavior_source(request,source_id):

    t = loader.get_template('suspicious_source_behavior_source.html')
    suspicious_behavior=SuspiciousSourceBehavior.objects.filter(source_id=source_id)
    c = {'suspicious_behavior': suspicious_behavior}
    return HttpResponse(t.render(c, request), content_type='text/html')

def suspicious_source_behavior_detail(request,s_id):

    t = loader.get_template('suspicious_source_behavior_detail.html')
    suspicious_behavior=SuspiciousSourceBehavior.objects.get(id=s_id)

    auth_succ_remote=Event_4624.objects.filter(sourceip=suspicious_behavior.source).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).order_by('time')
    auth_failed_remote = Event_4625.objects.filter(sourceip=suspicious_behavior.source).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).order_by('time')

    hosts_succ_remote=Event_4624.objects.filter(sourceip=suspicious_behavior.source).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).values('host').distinct()
    hosts_failed_remote = Event_4625.objects.filter(sourceip=suspicious_behavior.source).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(suspicious_behavior.start, suspicious_behavior.end)).values('host').distinct()

    unique_hosts=len(hosts_failed_remote)+len(hosts_succ_remote)

    c = {'suspicious_behavior': suspicious_behavior,'auth_failed_remote':auth_failed_remote,'auth_succ_remote':auth_succ_remote,'unique_hosts':unique_hosts}

    return HttpResponse(t.render(c, request), content_type='text/html')
