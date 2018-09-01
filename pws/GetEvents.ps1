$AuthEvents = Get-WinEvent -FilterHashtable @{Logname='Security';Id=4624}
$FailedAuthEvents = Get-WinEvent -FilterHashtable @{Logname='Security';Id=4625}
$LocalAuthEvents = Get-WinEvent -FilterHashtable @{Logname='Security';Id=4776}
$SpecialLogonEvents = Get-WinEvent -FilterHashtable @{Logname='Security';Id=4672}
$FileShareEvents = Get-WinEvent -FilterHashtable @{Logname='Security';Id=5140}

$ServiceEvents = Get-WinEvent -FilterHashtable @{Logname='System';Id=7045}
$SchTaskEvents = Get-WinEvent -FilterHashtable @{Logname='Security';Id=4698}

#To be able to read the log need to stop it
wevtutil set-log "Microsoft-Windows-WMI-Activity/Trace" /enabled:false
$WmiEvents =  Get-WinEvent -LogName Microsoft-Windows-WMI-Activity/Trace -Oldest
# start wmi logging
wevtutil set-log "Microsoft-Windows-WMI-Activity/Trace" /enabled:true /quiet:true /retention:false /maxsize:52428800

$hostname=$env:COMPUTERNAME

$AuthEvents2=@()
# Parse out the event message data
ForEach ($AuthEvent in $AuthEvents) {
    # Convert the event to XML
    $AuthEventXML = [xml]$AuthEvent.ToXml()
    # Iterate through each one of the XML message properties
    For ($i=0; $i -lt $AuthEventXML.Event.EventData.Data.Count; $i++) {
        # Append these as object properties
        Add-Member -InputObject $AuthEvent -MemberType NoteProperty -Force -Name  $AuthEventXML.Event.EventData.Data[$i].name -Value $AuthEventXML.Event.EventData.Data[$i].'#text'
    }
	$username= $AuthEvent.TargetUserName
	if ($username -ne "SYSTEM" -and $username -ne "ANONYMOUS LOGON" -and $username -ne "NETWORK SERVICE" -and $username -ne "LOCAL SERVICE" -and $username -ne $hostname+"$"){
		$AuthEvents2+=$AuthEvent

	}
}

$FailedAuthEvents2=@()
ForEach ($AuthFailEvent in $FailedAuthEvents) {
    $AuthFailEventXML = [xml]$AuthFailEvent.ToXml()
    For ($i=0; $i -lt $AuthFailEventXML.Event.EventData.Data.Count; $i++) {
        Add-Member -InputObject $AuthFailEvent -MemberType NoteProperty -Force -Name  $AuthFailEventXML.Event.EventData.Data[$i].name -Value $AuthFailEventXML.Event.EventData.Data[$i].'#text'
    }
	$username= $AuthFailEvent.TargetUserName
	if ($username -ne "SYSTEM" -and $username -ne "ANONYMOUS LOGON" -and $username -ne "NETWORK SERVICE" -and $username -ne "LOCAL SERVICE" -and $username -ne $hostname+"$"){
		$FailedAuthEvents2+=$AuthFailEvent

	}
}

$LocalAuthEvents2=@()
ForEach ($LocalAuthEvent in $LocalAuthEvents) {
    $LocalAuthEventXML = [xml]$LocalAuthEvent.ToXml()
    For ($i=0; $i -lt $LocalAuthEventXML.Event.EventData.Data.Count; $i++) {
        Add-Member -InputObject $LocalAuthEvent -MemberType NoteProperty -Force -Name  $LocalAuthEventXML.Event.EventData.Data[$i].name -Value $LocalAuthEventXML.Event.EventData.Data[$i].'#text'
    }
	$username= $LocalAuthEvent.TargetUserName
	if ($username -ne "SYSTEM" -and $username -ne "ANONYMOUS LOGON" -and $username -ne "NETWORK SERVICE" -and $username -ne "LOCAL SERVICE" -and $username -ne $hostname+"$"){
		$LocalAuthEvents2+=$LocalAuthEvent

	}
}



ForEach ($SEvent in $ServiceEvents) {
    $SeventXML = [xml]$SEvent.ToXml()
    For ($i=0; $i -lt $SeventXML.Event.EventData.Data.Count; $i++) {
        Add-Member -InputObject $SEvent -MemberType NoteProperty -Force -Name  $SeventXML.Event.EventData.Data[$i].name -Value $SeventXML.Event.EventData.Data[$i].'#text'
    }
}

ForEach ($SchTaskEvent in $SchTaskEvents) {
    $SchTaskEventXML = [xml]$SchTaskEvent.ToXml()
    For ($i=0; $i -lt $SchTaskEventXML.Event.EventData.Data.Count; $i++) {
        Add-Member -InputObject $SchTaskEvent -MemberType NoteProperty -Force -Name  $SchTaskEventXML.Event.EventData.Data[$i].name -Value $SchTaskEventXML.Event.EventData.Data[$i].'#text'
    }
}

$WmiEvents2=@()
ForEach ($WmiEvent in $WmiEvents) {
    $WmiEventXML = [xml]$WmiEvent.ToXml()
    For ($i=0; $i -lt $WmiEventXML.Event.EventData.Data.Count; $i++) {
        Add-Member -InputObject $WmiEvent -MemberType NoteProperty -Force -Name  $WmiEventXML.Event.EventData.Data[$i].name -Value $WmiEventXML.Event.EventData.Data[$i].'#text'
    }
	$wmiid= $WmiEvent.Id
	$msg= $WmiEvent.Message
	if (($wmiid -eq 2 -and $msg -like '*Win32_Process::Create*') -Or ($wmiid -eq 12 -and $msg -like '*Win32_Process::Create*')){
		$WmiEvents2 += $WmiEvent
	}
}

# View the results with your favorite output method

$AuthEvents2 = $AuthEvents2 | Select-Object TimeCreated, Id, MachineName, TargetUserName, LogonType, SubjectLogonId, ProcessName, IpAddress, WorkstationName,Status

$FailedAuthEvents2= $FailedAuthEvents2 | Select-Object TimeCreated, Id, MachineName, TargetUserName, LogonType, SubjectLogonId, ProcessName, IpAddress, WorkstationName, Status, SubStatus

$LocalAuthEvents2=$LocalAuthEvents2 | Select-Object TimeCreated,Id,MachineName,TargetUserName,Status

$ServiceEvents = $ServiceEvents | Select-Object TimeCreated, Id, MachineName, ServiceName, ImagePath,ServiceType

$SchTaskEvents = $SchTaskEvents | Select-Object TimeCreated, Id, MachineName, SubjectLogonId, TaskName,TaskContent

$WmiEvents2 = $WmiEvents2 | Select-Object TimeCreated,Id,MachineName,Message

$EventsAll=@()
$EventsAll+=$AuthEvents2
$EventsAll+=$FailedAuthEvents2
$EventsAll+=$LocalAuthEvents2
$EventsAll+=$SpecialLogonEvents2
$EventsAll+=$ServiceEvents
$EventsAll+=$SchTaskEvents
$EventsAll+=$WmiEvents2
$EventsAll+=$FileShareEvents

$hostname=$env:computername
$path="\\path\\events"
$filename=$hostname+".csv"
$final=Join-Path $path $filename

$EventsAll | Select-Object TimeCreated, Id, MachineName, TargetUserName, SubjectUserName, LogonType, SubjectLogonId, Status,SubStatus, ProcessName, IpAddress, WorkstationName, PrivilegeList, ServiceName, ImagePath,ServiceType,TaskName,TaskContent,Message, ShareName, KeywordsDisplayNames  | Export-Csv -NoTypeInformation $final