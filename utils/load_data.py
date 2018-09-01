import csv
import django
import os, sys
import re
from datetime import datetime

#utils folder
proj_path = os.path.dirname(os.getcwd())
sys.path.append(proj_path)
#utils folder

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LM_Hunting.settings")

django.setup()
from Oriana.models import *
from utils import getlogontype,find_between,getdate

TIME_IDX=-1
ID_IDX=-1
MACHINENAME_IDX=-1
TARGETUSERNAME_IDX=-1
SUBJECTUSERNAME_IDX=-1
LOGONTYPE_IDX=-1
STATUS_IDX=-1
SUBSTATUS_IDX=-1
PROCESSNAME_IDX=-1
IP_IDX=-1
WORKSTATIONAME_IDX=--1
SERVICENAME_IDX=-1
IMAGEPATH_IDX=-1
SERVICETYPE_IDX=-1
TASKNAME_IDX=-1
TASKCONTENT_IDX=-1
MESSAGGE_IDX=-1
SHARENAME_IDX=-1
PRIVILEGE_IDX=-1




def load_data(folderpath):
    """
    Open CSV files in a folder and index the data.
    """
    files=os.listdir(folderpath)

    for f in files:

        fullname = folderpath + f
        if os.path.isfile(fullname):
            with open(fullname, 'rb') as csvfile:

                eventsreader = csv.reader(csvfile, delimiter=',', quotechar='"')
                for line, row in enumerate(eventsreader):
                    if line==0:
                        for column in range(0,len(row)):
                            if  row[column] == "TimeCreated":
                                TIME_IDX=column
                            elif row[column] == "Id":
                                ID_IDX=column
                            elif row[column] == "MachineName":
                                MACHINENAME_IDX=column
                            elif row[column] == "TargetUserName":
                                TARGETUSERNAME_IDX = column
                            elif row[column] == "SubjectUserName":
                                SUBJECTUSERNAME_IDX = column
                            elif row[column] == "LogonType":
                                LOGONTYPE_IDX = column
                            elif row[column] == "ProcessName":
                                PROCESSNAME_IDX = column
                            elif row[column] == "IpAddress":
                                IP_IDX = column
                            elif row[column] == "WorkstationName":
                                WORKSTATIONAME_IDX = column
                            elif row[column] == "ServiceName":
                                SERVICENAME_IDX = column
                            elif row[column] == "ImagePath":
                                IMAGEPATH_IDX = column
                            elif row[column] == "ServiceType":
                                SERVICETYPE_IDX = column
                            elif row[column] == "Status":
                                STATUS_IDX = column
                            elif row[column] == "SubStatus":
                                SUBSTATUS_IDX = column
                            elif row[column] == "TaskName":
                                TASKNAME_IDX = column
                            elif row[column] == "TaskContent":
                                TASKCONTENT_IDX = column
                            elif row[column] == "Message":
                                MESSAGGE_IDX = column
                            elif row[column] == "ShareName":
                                SHARENAME_IDX = column
                            elif row[column] == "PrivilegeList":
                                PRIVILEGE_IDX = column

                    print "reading ",f," line:",line
                    #4624 Authentication event
                    if row[ID_IDX] == "4624":
                        strtime = row[TIME_IDX]
                        time=getdate(strtime)

                        hostname = row[MACHINENAME_IDX]
                        username = row[TARGETUSERNAME_IDX].lower()
                        logontype=getlogontype(str(row[LOGONTYPE_IDX]))
                        processname = row[PROCESSNAME_IDX]
                        sourceip=row[IP_IDX]
                        sourcehost=row[WORKSTATIONAME_IDX]

                        host, created_host = Host.objects.get_or_create(hostname=hostname)
                        user, created_user = User.objects.get_or_create(username=username)

                        if (logontype == "Network" or logontype == "RemoteInteractive") and (sourceip != "-" and ":" not in sourceip):
                            source, created_source=SourceIp.objects.get_or_create(sourceip=sourceip,hostname=sourcehost)
                            event4624, createdevent = Event_4624.objects.get_or_create(time=time, host=host, user=user,logontype=logontype,processname=processname,sourcehost=sourcehost,sourceip=source)
                        else:
                            try:
                                event4624, createdevent = Event_4624.objects.get_or_create(time=time, host=host, user=user,logontype=logontype,processname=processname,sourcehost=sourcehost)
                            except:
                                pass
                        if createdevent:
                            print "new 4624 created for host "+hostname

                    # 4625 Authentication event
                    if row[ID_IDX] == "4625":
                        strtime = row[TIME_IDX]
                        time = getdate(strtime)
                        hostname = row[MACHINENAME_IDX]
                        username = row[TARGETUSERNAME_IDX].lower()
                        logontype = getlogontype(str(row[LOGONTYPE_IDX]))
                        processname = row[PROCESSNAME_IDX]
                        sourceip = row[IP_IDX]
                        sourcehost = row[WORKSTATIONAME_IDX]
                        status = row[STATUS_IDX]
                        substatus = row[SUBSTATUS_IDX]

                        host, created_host = Host.objects.get_or_create(hostname=hostname)
                        user, created_user = User.objects.get_or_create(username=username)

                        #new
                        if (logontype == "Network" or logontype == "RemoteInteractive") and (sourceip != "-" and ":" not in sourceip ):
                            source, created_source=SourceIp.objects.get_or_create(sourceip=sourceip,hostname=sourcehost)
                            event4625, createdevent = Event_4625.objects.get_or_create(time=time, host=host, user=user,logontype=logontype,processname=processname,sourcehost=sourcehost,sourceip=source,status=status,substatus=substatus)
                        else:
                            event4625, createdevent = Event_4625.objects.get_or_create(time=time, host=host, user=user,logontype=logontype,processname=processname,sourcehost=sourcehost,status=status,substatus=substatus)

                        if createdevent:
                            print "new 4625 created for host " + hostname

                    # 4776 Local Authentication Event
                    if row[ID_IDX] == "4776":
                        strtime = row[TIME_IDX]
                        time = getdate(strtime)

                        hostname = row[MACHINENAME_IDX]
                        username = row[TARGETUSERNAME_IDX].lower()
                        status = row[STATUS_IDX]

                        host, created_host = Host.objects.get_or_create(hostname=hostname)
                        user, created_user = User.objects.get_or_create(username=username)

                        event4776, createdevent = Event_4776.objects.get_or_create(time=time, host=host, user=user,status=status)
                        if createdevent:
                            print "new 4776 created for host " + hostname

                    # 5140 File Share Event
                    if row[ID_IDX] == "5140":
                        strtime = row[TIME_IDX]
                        time = getdate(strtime)

                        hostname = row[MACHINENAME_IDX]
                        username = row[SUBJECTUSERNAME_IDX].lower()
                        sharename = row[SHARENAME_IDX]

                        host, created_host = Host.objects.get_or_create(hostname=hostname)
                        user, created_user = User.objects.get_or_create(username=username)

                        event5140, createdevent = Event_5140.objects.get_or_create(time=time, host=host, user=user,sharename=sharename)
                        if createdevent:
                            print "new 5140 created for host " + hostname


                    # 4672 Privileged Auth
                    if row[ID_IDX] == "4672":
                        strtime = row[TIME_IDX]
                        time = getdate(strtime)

                        hostname = row[MACHINENAME_IDX]
                        username = row[SUBJECTUSERNAME_IDX].lower()
                        privilegelist = row[PRIVILEGE_IDX]

                        host, created_host = Host.objects.get_or_create(hostname=hostname)
                        user, created_user = User.objects.get_or_create(username=username)

                        event4672, createdevent = Event_4672.objects.get_or_create(time=time, host=host, user=user,privilegelist=privilegelist)
                        if createdevent:
                            print "new 4672 created for host " + hostname

                    # 7045 New Service created event
                    elif row[ID_IDX] == "7045":

                        strtime = row[TIME_IDX]
                        time = getdate(strtime)
                        hostname = row[MACHINENAME_IDX]
                        servicename=row[SERVICENAME_IDX]
                        imagepath=row[IMAGEPATH_IDX]
                        servicetype=row[SERVICETYPE_IDX]

                        service,service_created = Service.objects.get_or_create(servicename=servicename, imagepath=imagepath, servicetype=servicetype)
                        host, created_host = Host.objects.get_or_create(hostname=hostname)
                        event7045,createdevent=Event_7045.objects.get_or_create(time=time, host=host, service=service)
                        if createdevent:
                            print "new 7045 created for "+hostname

                    # 4698 New Scheduled Task event
                    elif row[ID_IDX] == "4698":

                        strtime = row[TIME_IDX]
                        time = getdate(strtime)

                        hostname = row[MACHINENAME_IDX]
                        taskname= row[TASKNAME_IDX]
                        taskdetails= row[TASKCONTENT_IDX]
                        #arguments = re.findall('<Arguments>(.*?)</Arguments>', taskdetails, re.DOTALL)[0]
                        #cmdline = re.findall('<Command>(.*?)</Command>', taskdetails, re.DOTALL)[0]
                        try:
                            arguments = find_between(taskdetails,"<Arguments>","</Arguments>")
                        except:
                            arguments =""
                        try:
                            cmdline= find_between(taskdetails, "<Command>", "</Command>")
                        except:
                            cmdline= ""
                        host, created_host = Host.objects.get_or_create(hostname=hostname)
                        task,taskcreated = Task.objects.get_or_create(taskname=taskname,imagepath=cmdline,arguments=arguments)
                        event4698,createdevent=Event_4698.objects.get_or_create(time=time, host=host, task=task)
                        if createdevent:
                            print "new 4698 created for " + hostname

                    # WMI event
                    elif row[ID_IDX] == "2":

                        strtime = row[TIME_IDX]
                        time = getdate(strtime)

                        hostname = row[MACHINENAME_IDX]
                        wmidetails= row[MESSAGGE_IDX]
                        operationid = re.findall('GroupOperationId = (.*?);', wmidetails, re.DOTALL)[0]
                        operation = re.findall('Operation = (.*?);', wmidetails, re.DOTALL)[0]
                        host, created_host = Host.objects.get_or_create(hostname=hostname)
                        WmiEvent_2.objects.create(time=time, host=host, operationid=operationid,operation=operation)
                        print "new Wmi Event 2 created for " + hostname