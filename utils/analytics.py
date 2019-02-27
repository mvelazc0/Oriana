import django
from django.db.models import Q
import os, sys
from datetime import timedelta
from datetime import date

from utils import *

#utils folder
proj_path = os.path.dirname(os.getcwd())
sys.path.append(proj_path)
#utils folder

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LM_Hunting.settings")
django.setup()

from Oriana.models import *

def CalculateUserTotals():
    """Calculates a user's statistics based on authentication events"""

    print "*** Calculate User Totals ***"

    users=User.objects.all()

    for u in users:

        failed_auth_events = Event_4625.objects.filter(user=u)

        succ_auth_events=Event_4624.objects.filter(user=u)
        unique_succ_remote_hosts=Event_4624.objects.filter(user=u).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('host').distinct()
        unique_succ_local_hosts = Event_4624.objects.filter(user=u).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('host').distinct()

        unique_succ_rdp_hosts = Event_4624.objects.filter(user=u).filter(Q(logontype="RemoteInteractive")).values('host').distinct()
        unique_succ_network_hosts = Event_4624.objects.filter(user=u).filter(Q(logontype="Network")).values('host').distinct()

        unique_failed_remote_hosts=Event_4625.objects.filter(user=u).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('host').distinct()

        u.succ_auth_events=len(succ_auth_events)
        u.failed_auth_events = len(failed_auth_events)
        u.unique_succ_remote_hosts= len(unique_succ_remote_hosts)
        u.unique_failed_remote_hosts = len(unique_failed_remote_hosts)
        u.unique_succ_rdp_hosts = len(unique_succ_rdp_hosts)
        u.unique_succ_network_hosts = len(unique_succ_network_hosts)
        u.unique_succ_local_hosts = len(unique_succ_local_hosts)
        u.save()

        print u.username," total events:",len(succ_auth_events)," uniquer remote hosts:",len(unique_succ_remote_hosts)," and ",len(unique_succ_local_hosts)," uniquer local hosts"


def CalculateHostTotals():
    """Calculates a host's statistics based on authentication events"""

    print "*** Calculate Host Totals ***"

    hosts=Host.objects.all()
    for h in hosts:
        total_succ_auths=Event_4624.objects.filter(host=h)
        total_failed_auths=Event_4625.objects.filter(host=h)

        unique_succ_remote_users=Event_4624.objects.filter(host=h).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('user').distinct()
        unique_succ_local_users = Event_4624.objects.filter(host=h).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('user').distinct()

        unique_failed_remote_users = Event_4625.objects.filter(host=h).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('user').distinct()
        unique_failed_local_users = Event_4624.objects.filter(host=h).exclude(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('user').distinct()

        h.total_succ_auths=len(total_succ_auths)
        h.total_failed_auths=len(total_failed_auths)
        h.unique_succ_remote_users= len(unique_succ_remote_users)
        h.unique_succ_local_users = len(unique_succ_local_users)
        h.unique_failed_remote_users=len(unique_failed_remote_users)
        h.unique_failed_local_users=len(unique_failed_local_users)

        h.save()

        print h.hostname," total events:",len(total_succ_auths)," uniquer remote users:",len(unique_succ_remote_users)," and ",len(unique_succ_local_users)," unique local users"

def CalculateSourceIpTotals():
    """Calculates a source ip's statistics based on authentication events"""

    sources=SourceIp.objects.all()

    for s in sources:

        total_succ_auths = Event_4624.objects.filter(sourceip=s)
        total_failed_auths = Event_4625.objects.filter(sourceip=s)

        unique_succ_remote_hosts = Event_4624.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('host').distinct()
        unique_failed_remote_hosts = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).values('host').distinct()

        s.total_succ_auths=len(total_succ_auths)
        s.total_failed_auths = len(total_failed_auths)
        s.unique_succ_remote_hosts = len(unique_succ_remote_hosts)
        s.unique_failed_remote_hosts = len(unique_failed_remote_hosts)

        print s, "totals :"," succ_auths:",str(len(total_succ_auths))," failed_authts:",str(len(total_failed_auths))," unique_remote_hosts:",str(len(unique_succ_remote_hosts))," unique_failed_remote_hosts:",str(len(unique_succ_remote_hosts))

        s.save()


def CalculateServiceTotals():
    """
    Calculates the frequency of all Services
    Calculates the N-Gram score of all Service names
    """

    print "*** Calculate Service Totals ***"

    service_events=Event_7045.objects.all()
    services=[]
    for se in service_events:
        services.append(se.service)
    fanalysis = Counter(services)
    for k, v in fanalysis.items():
        k.count=v
        k.save()

    services = Service.objects.all()
    servicenames = []
    for svc in services:
        servicenames.append(svc.servicename)
    unique_servicenames = list(set(servicenames))
    ngram_weights= calculate_weights(2, unique_servicenames)

    services = Service.objects.all()
    for svc in services:
        svc.ngramscore=score(2, svc.servicename, ngram_weights)
        svc.save()

def CalculateTaskTotals():
    """
    Calculates the frequency of all Tasks
    Calculates the Ngram score of all Task Names
    """
    print "*** Calculate Task Totals ***"

    task_events=Event_4698.objects.all()
    tasks=[]
    for te in task_events:
        tasks.append(te.task)

    fanalysis= Counter(tasks)
    for k, v in fanalysis.items():
        k.count=v
        k.save()


    tasks = Task.objects.all()
    tasknames =[]
    for t in tasks:
        tasknames.append(t.taskname)
    uniquetasknames=list(set(tasknames))
    ngram_weights= calculate_weights(2, uniquetasknames)
    tasks = Task.objects.all()
    for t in tasks:
        t.ngramscore=score(2, t.taskname, ngram_weights)
        t.save()

def CalculateCmdlineTotals():
    """Calculates the frequency the ImagePath field from 7045 ( Service Creation ) and 4698 (New Task Created ) events"""

    print "*** Calculate Cmdline Totals ***"

    cmdlines=[]

    services=Event_7045.objects.all()
    tasks=Event_4698.objects.all()

    for s in services:
        cmdlines.append(s.service.imagepath)

    for t in tasks:
        cmdlines.append(t.task.imagepath+t.task.arguments)

    fanalysis=Counter(cmdlines)

    for k,v in fanalysis.items():

        FA_imagepath.objects.create(imagepath=k,count=v,characterscount=len(k))


def PossibleLM_SchTask():
    """Identifies possible LM events based on a Scheduled Task being created right after a remote authentication 4624"""

    print "*** Identify Possible Task Based Lateral Movement Events ***"

    task_creations = Event_4698.objects.exclude(task__taskname__contains="Arellia").exclude(task__imagepath__contains="ProgramData")
    for t in task_creations :

        host=t.host
        time=t.time
        #print "reviewing: "+host.hostname
        min_time=time - timedelta(seconds=30)
        max_time = time

        logins = Event_4624.objects.filter(host=host, logontype="Network", time__range=(min_time, max_time)).exclude(user__username__contains="$")
        if len(logins) > 0:
            login=logins.first()
            PossibleLM.objects.create(event_4698=t, auth=login, reason="Scheduled Task")
            print "created suspicious task event on host " + host.hostname

def PossibleLM_Service():
    """Identifies possible LM events based on a Service being created right after a remote authentication 4624"""

    print "*** Identify Possible Service Based Lateral Movement Events ***"

    service_creations = Event_7045.objects.all()

    for s in service_creations:

        host=s.host
        time=s.time
        #print "reviewing: " + host.hostname
        min_time=time - timedelta(seconds=30)
        max_time= time
        ## Whitelists
        logins = Event_4624.objects.filter(host=host,logontype="Network",time__range=(min_time,max_time)).exclude(user__username__contains="$")

        if len(logins) > 0:
            login=logins.first()
            PossibleLM.objects.create(event_7045=s, auth=login, reason="Create Service")
            print "created suspicious service event on host " + host.hostname


def PossibleLM_Wmi():
    """Identifies possible LM events based on a WMI Event 2 being created right after a remote authentication 4624"""

    print "*** Identify Possible WMI Based Lateral Movement Events ***"

    wmi_events = WmiEvent_2.objects.all()
    already_reviewed = []
    for wmi in wmi_events :

        host=wmi.host
        time=wmi.time
        print "using wmievent ", wmi.id, " with host:",host.hostname," at:",time

        timestamp=str(time.year)+":"+str(time.day)+":"+str(time.hour)+":"+str(time.minute)+":"+host.hostname

        if timestamp not in already_reviewed:

            #print time," timestamp not in already vieweed,entering"

            already_reviewed.append(timestamp)
            min_time=time - timedelta(seconds=30)
            max_time = time
            logins = Event_4624.objects.filter(host=host,logontype="Network",time__range=(min_time,max_time)).exclude(user__username__contains="$")
            if len(logins) > 0:
                #print "found ",str(len(logins))
                login=logins.first()
                PossibleLM.objects.create(event_wmi_2=wmi, auth=login, reason="WMI Execution")
                print "created suspicious Wmi exec event for: " + host.hostname



def LM_Sessions():
    """Identifies  lateral movement sessions based on possible lateral movement events"""

    print "*** Identify Possible Lateral Movement Sessions***"

    first=PossibleLM.objects.all().order_by('auth__time').first()
    last = PossibleLM.objects.all().order_by('auth__time').last()

    try:
        starttime=first.auth.time
        finishtime = last.auth.time
    except:
        # No possible Latearal movement events
        return

    mid = starttime + timedelta(minutes=120)
    start1=starttime

    while (finishtime >= start1):

        #print "search from : "+str(start1), "to :"+str(mid)
        others = PossibleLM.objects.filter(auth__time__range=(start1, mid)).order_by('auth__time')
        if len(others) > 1:
            #print len(others)

            events=[]
            users=[]
            hosts=[]

            for s in others:
                users.append(s.auth.user)
                hosts.append(s.auth.host)
                events.append(s)

            breach = PossibleLmSession(start=start1, end=mid, delta=str(mid - start1), hosts=len(list(set(hosts))), users=len(list(set(users))))
            breach.save()
            breach.attacks.set(events)
            print "created possible Lateral Movement session"

        start1 = start1 + timedelta(minutes=120)
        mid = mid + timedelta(minutes=120)


def SuspiciousUserBehavior_1():
    """
    Insufficient Privileges
    A user is failing to authenticate to a large number of hosts due to insufficient privileges for the requested logon type
    """
    print "*** Running Suspicious User Behavior #1 Analytics ***"

    # This will return a list of users who have failed to authenticate to more than 3 hosts.
    # TODO: This should be configured through the UI
    users = User.objects.filter(unique_failed_remote_hosts__gt=3)

    for u in users:
        #print u
        print '.',
        ## TODO: A user may have 4625 events to more than 15 unique hosts, but without a 0xc000015b subtatus.
        ## Need to avoid the try,except
        try:
            start = Event_4625.objects.filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(user=u).filter(status='0xc000015b').order_by('time').first().time
            finish = Event_4625.objects.filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(user=u).filter(status='0xc000015b').order_by('time').last().time
        except:
            #print "skip for with ",u
            continue

        mid = start + timedelta(minutes=120)
        start1 = start

        while (finish >= start1):

            failed_auths = Event_4625.objects.filter(user=u).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(status='0xc000015b').filter(time__range=(start1, mid)).order_by('time')
            unique_hosts= Event_4625.objects.filter(user=u).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(status='0xc000015b').filter(time__range=(start1, mid)).values('host').distinct()

            if len(failed_auths)>0 and len(unique_hosts)>10:

                #print "found, failed logons:",str(len(failed_auths))," on ",str(len(unique_hosts))," hosts."
                name="User: Privilege Enumeration"
                descr="Legitimate credentials have been used to authenticate to a large number of hosts but authentication failed due to lack of privileges on the destination host.\nThis behavior could represent an attacker trying to identify privileges across the environment"
                suspicious_behavior=SuspiciousUserBehavior(name=name,description=descr,user=u,start=start1,end=mid)
                suspicious_behavior.save()
                print "suspicious user behavior #1 created for user ",u


            start1 = start1 + timedelta(minutes=120)
            mid = mid + timedelta(minutes=120)


def SuspiciousUserBehavior_2():
    """
    High Number of Destinations
    A user is successfully authenticating to a large number of hosts
    """
    print "*** Running Suspicious User Behavior #2 Analytics ***"

    # This will return a list of users who have successfully authenticated to more than 3 hosts.
    # TODO: This should be configured through the UI
    users = User.objects.filter(unique_succ_remote_hosts__gt=3)
    for u in users:
        #print u," ",str(u.id)
        print ".",
        start = Event_4624.objects.filter(user=u).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time').first().time
        finish = Event_4624.objects.filter(user=u).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time').last().time

        mid = start + timedelta(minutes=120)
        start1 = start

        while (finish >= start1):
            auths = Event_4624.objects.filter(user=u).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(start1, mid)).order_by('time')
            unique_hosts = Event_4624.objects.filter(user=u).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(start1, mid)).values('host').distinct()

            if len(auths)>0 and len(unique_hosts)>10:

                #print "found, failed logons:",str(len(auths))," on ",str(len(unique_hosts))," hosts."
                name = "User: High number of destinations"
                descr = "Legitimate credentials have been used to successfully authenticate to a large number of hosts. This behavior could represent an attacker moving laterally"
                suspicious_behavior = SuspiciousUserBehavior(name=name, description=descr, user=u, start=start1,end=mid)
                suspicious_behavior.save()
                print "suspicious user behavior #2 created for user ",u

            start1 = start1 + timedelta(minutes=120)
            mid = mid + timedelta(minutes=120)

def SuspiciousUserBehavior_3():
    """
    Roaming User
    A user account is locally authenticating on several hosts
    """
    print "*** Running Suspicious User Behavior #3 Analytics ***"

    # This will return a list of users who locally logged in to more than 3 hosts.
    # TODO: This should be configured through the UI
    users=User.objects.filter(unique_succ_local_hosts__gt=3)
    for u in users:
        #print u," ",str(u.id)
        print ".",

        ## TODO
        try:
            start = Event_4624.objects.filter(user=u).exclude(logontype="Network").exclude(logontype="RemoteInteractive").exclude(logontype="Service").order_by('time').first().time
            finish = Event_4624.objects.filter(user=u).exclude(logontype="Network").exclude(logontype="RemoteInteractive").exclude(logontype="Service").order_by('time').last().time
        except:
            continue

        mid = start + timedelta(minutes=120)
        start1 = start

        while (finish >= start1):
            auths = Event_4624.objects.filter(user=u).exclude(logontype="Network").exclude(logontype="RemoteInteractive").exclude(logontype="Service").filter(time__range=(start1, mid)).order_by('time')
            unique_hosts = Event_4624.objects.filter(user=u).exclude(logontype="Network").exclude(logontype="RemoteInteractive").exclude(logontype="Service").filter(time__range=(start1, mid)).values('host').distinct()

            if len(auths)>0 and len(unique_hosts)>10:
                #print "found, logons:",str(len(auths))," on ",str(len(unique_hosts))," hosts."
                name="User: Roaming Authentication"
                descr="A user locally logs in to several computers in an interval of time. This behavior could this could mean password sharing or credential theft."
                suspicious_behavior = SuspiciousUserBehavior(name=name, description=descr, user=u, start=start1,end=mid)
                suspicious_behavior.save()
                print "suspicious user behavior #3 created for user ",u

            start1 = start1 + timedelta(minutes=120)
            mid = mid + timedelta(minutes=120)

def SuspiciousUserBehavior_4():
    """
    Local Account spray
    A local user account is trying to authenticating to a large number of hosts.
    """

    print "*** Running Suspicious User Behavior #4 Analytics ***"

    local_auths=Event_4776.objects.all()

    users=[]
    for l in local_auths:

        users.append(l.user)

    users = list(set(users))
    for u in users:
        #print u, " ", str(u.id)
        print ".",
        ## TODO
        try:
            start = Event_4776.objects.filter(user=u).order_by('time').first().time
            finish = Event_4776.objects.filter(user=u).order_by('time').last().time
        except:
            continue

        mid = start + timedelta(minutes=120)
        start1 = start

        while (finish >= start1):
            auths = Event_4776.objects.filter(user=u).filter(time__range=(start1, mid)).order_by('time')
            unique_hosts = Event_4776.objects.filter(user=u).filter(time__range=(start1, mid)).values('host').distinct()

            if len(auths) > 0 and len(unique_hosts) > 2:
                #print "between ", str(start1), "and ", str(mid)
                #print "found local auths:", str(len(auths)), " on ", str(len(unique_hosts)), " hosts."

                name = "User: Local Account Usage"
                descr = "A non-domain accoint is being used to authenticate to more than 2 hosts in a short period of time. This behavior could represent an attacker trying to move laterally with local accunts"
                suspicious_behavior = SuspiciousUserBehavior(name=name, description=descr, user=u, start=start1,end=mid)
                suspicious_behavior.save()
                print "suspicious user behavior #4 created for user ",u

            start1 = start1 + timedelta(minutes=120)
            mid = mid + timedelta(minutes=120)


def SuspiciousSourceIpBehavior_1():

    ## Possible User Enumeration
    ## A source host is failing to:  authenticate fake users that dont exist ( SubStatus 0xC0000064 )

    print "*** Running Suspicious Source Host Behavior #1 Analytics ***"

    sources = SourceIp.objects.filter(unique_failed_remote_hosts__gt=0)
    for s in sources:

        #print s,str(s.id)
        print ".",
        #TODO: Some hosts may have failed_remote_hosts greather than 0 but not have 0xc00000064 so this fails
        try:
            start = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(substatus="0xc0000064").order_by('time').first().time
            finish = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(substatus="0xc0000064").order_by('time').last().time

        except:
            continue

        mid = start + timedelta(minutes=120)
        start1 = start

        while (finish >= start1):
            #print "searching on host:",str(s)," between:",str(start1)," and ",str(mid)
            auths = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(substatus="0xc0000064").filter(time__range=(start1, mid)).order_by('time')
            unique_users = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(substatus="0xc0000064").filter(time__range=(start1, mid)).values('user').distinct()

            if len(auths)>0 and len(unique_users)>1:
                #print "found, logons:",str(len(auths))," on ",str(len(unique_users))," users."
                name="Source Host: Possible User Enumeration"
                descr="A source host is failing to authenticate  with several users non existing users. This behavior could represent and attacker  trying to enumerate legitimate users."
                suspicious_behavior = SuspiciousSourceBehavior(name=name, description=descr, source=s, start=start1,end=mid)
                suspicious_behavior.save()
                print "suspicious source computer behavior #1 created for source", s

            start1 = start1 + timedelta(minutes=120)
            mid = mid + timedelta(minutes=120)


def SuspiciousSourceIpBehavior_2():

    ## Possible Password Spray/Brute Force Attack
    ## several users failing auth from one source ip address in an interval of time (SubStatus 0xc000006a )

    print "*** Running Suspicious Source Host Behavior #2 Analytics ***"

    sources = SourceIp.objects.filter(unique_failed_remote_hosts__gt=0)
    #print len(sources)
    for s in sources:
        #print s," ",str(s.id)
        print ".",
        try:
            start = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(substatus="0xc000006a").order_by('time').first().time
            finish = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(substatus="0xc000006a").order_by('time').last().time
            #print start
            #print finish
        except:
            #print "failed with ",s," ",str(s.id)
            continue

        #print s
        mid = start + timedelta(minutes=120)
        start1 = start
        while (finish >= start1):
            auths = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(substatus="0xc000006a").filter(time__range=(start1, mid)).order_by('time')
            unique_users = Event_4625.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(substatus="0xc000006a").filter(time__range=(start1, mid)).values('user').distinct()

            if len(auths)>0 and len(unique_users)>1:
                #print "\tfound, logons:",str(len(auths))," on ",str(len(unique_users))," users."
                name="Source Host: Possible Password Spray/Brute Force"
                descr="A source host is failing to authenticate (wrong password) with several users in a short period of time interval of time. This behavior can represent a password spray attack."
                suspicious_behavior = SuspiciousSourceBehavior(name=name, description=descr, source=s, start=start1,end=mid)
                suspicious_behavior.save()
                print "suspicious source computer behavior #1 created for source", s


            start1 = start1 + timedelta(minutes=120)
            mid = mid + timedelta(minutes=120)


def SuspiciousSourceIpBehavior_3():

    ## High number of users
    ## A source computer is successfully authenticating with a high number of users. This behavior can represent an attacker that has compromised several accounts and using them to move laterally.

    print "*** Running Suspicious Source Host Behavior #3 Analytics ***"

    sources = SourceIp.objects.filter(unique_succ_remote_hosts__gt=0)
    for s in sources:
        print ".",
        try:
            start = Event_4624.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time').first().time
            finish = Event_4624.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).order_by('time').last().time
        except:
            continue

        mid = start + timedelta(minutes=120)
        start1 = start

        while (finish >= start1):
            auths = Event_4624.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(start1, mid)).order_by('time')
            unique_users = Event_4624.objects.filter(sourceip=s).filter(Q(logontype="Network") | Q(logontype="RemoteInteractive")).filter(time__range=(start1, mid)).values('user').distinct()

            if len(auths)>0 and len(unique_users)>2:
                #print s
                #print "found, logons:",str(len(auths))," on ",str(len(unique_users))," users."
                name="Source Host: High number of users"
                descr="A source computer is successfully authenticating with a high number of users. This behavior can represent an attacker that has compromised several accounts and using them to move laterally."
                suspicious_behavior = SuspiciousSourceBehavior(name=name, description=descr, source=s, start=start1,end=mid)
                suspicious_behavior.save()
                print "suspicious source computer behavior #3 created for source", s

            start1 = start1 + timedelta(minutes=120)
            mid = mid + timedelta(minutes=120)


def runall():

    CalculateUserTotals()
    CalculateHostTotals()
    CalculateSourceIpTotals()
    CalculateServiceTotals()
    CalculateTaskTotals()
    CalculateCmdlineTotals()
    PossibleLM_Service()
    PossibleLM_SchTask()
    PossibleLM_Wmi()
    LM_Sessions()
    SuspiciousUserBehavior_1()
    SuspiciousUserBehavior_2()
    SuspiciousUserBehavior_3()
    SuspiciousUserBehavior_4()
    SuspiciousSourceIpBehavior_1()
    SuspiciousSourceIpBehavior_2()
    SuspiciousSourceIpBehavior_3()


