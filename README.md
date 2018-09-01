# Oriana
Oriana is a threat hunting tool that leverages a subset of Windows events to build relationships, calculate totals and  run analytics. The results are presented in a Web layer to help defenders identify outliers and suspicious behavior on corporate environments.

Oriana was built using Python, the Django Web Framework, the Postgres database and Bootstrap. The Windows Event exporting script was written in PowerShell.

## Quick Start Guide

### Prerequisites

#### On Windows

```
Download & install Python 2.7 https://www.python.org/downloads/
Download & install Postgres https://www.postgresql.org/download/windows/
```

#### On Linux

```
sudo apt-get install postgresql postgresql-contrib
```


### Installation


```
git clone https://github.com/mvelazc0/Oriana.git
pip install -r Oriana/requirements.txt
```

## Hunting

### Export Events

Oriana relies on a PowerShell script to export certain Windows events into CSV files. The files will be written to a network share specified on the source code (dont forget to change this !) that can then be loaded into the database for indexing and analysis. The script needs to run in the context of an Administrator and can be deployed in different ways:

* Using a software deployment platform like SSCM
* Command Execution through an agent
 ```
 powershell.exe -File \\path\GetEvents.ps1 
 ```
* Powershell Remoting
```
 Invoke-Command -ComputerName PC1,PC2 -FilePath C:\path\GetEvents.ps1 
 ```

### Setup Database

 ```
 python oriana.py -A createdb
 python oriana.py -A startdb
 ```
**createdb** will ask for a Postgres username/password and will create a database as well as update the Django configuration files that allow it to connect to Postgres.
**Note:** settings.py will contain the password in clear text.

**startdb** will initialize oriana's database schema.

 ### Load Events
 
 ```
 python oriana.py -A load -d [path_to_logs]
 ```
 The **load** action will read the CSV files located on the path and store all events in the database.
 
 ### Run Analytics

 ```
 python oriana.py -A analytics
```
Analytics details will be added to the Wiki.

 ### Start Web Server

 ```
 python oriana.py -A runserver
 ```
 Oriana will run on port 8080 of the loopback interface
 http://127.0.0.1:8000

Happy Hunting !


## Authors

* **Mauricio Velazco** - [@mvelazco](https://twitter.com/mvelazco)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details
