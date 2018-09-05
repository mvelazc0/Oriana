# Oriana
Oriana is a threat hunting tool that leverages a subset of Windows events to build relationships, calculate totals and  run analytics. The results are presented in a Web layer to help defenders identify outliers and suspicious behavior on corporate environments.

Oriana was built using Python, the Django Web Framework, the Postgres database and Bootstrap. The Windows Event exporting script was written in PowerShell.

## Quick Start Guide / Docker Configuration

### Prerequisites

- [Have docker installed](https://docs.docker.com/install/)
- Have git installed
- [Docker-compose installed & working](https://docs.docker.com/compose/install/)

Clone the repo

```
git clone https://github.com/mvelazc0/Oriana.git
pip install -r Oriana/requirements.txt
```

### Docker

Go into the working folder of Oriana */Oriana* and not *~~/Oriana/Oriana/~~*

```commandline
cd Oriana
```

First we build the docker containers, and then run them. *(If you get an error about docker-compose being installed, in your terminal run *`pip install docker-compose`*)*.

And once setup view Oriana at `http://127.0.0.1:8000`.

```commandline
docker-compose build
docker-compose up
```

Once you have completed this, you should have seen something like the below scroll through your terminal.

```commandline
(Oriana) desktop# docker-compose build
postgres uses an image, skipping
Building web
Step 1/9 : FROM python:2.7
 ---> 17c0fe4e76a5
Step 2/9 : ENV PYTHONBUFFERED 1
...
Successfully built 94223655db0d
Successfully tagged web:latest
nginx uses an image, skipping

(Oriana) desktop# docker-compose up   
Starting oriana-docker_postgres_1  ... done
Recreating oriana-docker_web_1     ... done
Recreating oriana-docker_nginx_1   ... done
...
web_1       | ________        .__                      
web_1       | \_____  \_______|__|____    ____ _____   
web_1       |  /   |   \_  __ \  \__  \  /    \__  \  
web_1       | /    |    \  | \/  |/ __ \|   |  \/ __ \_
web_1       | \_______  /__|  |__(____  /___|  (____  /
web_1       |         \/              \/     \/     \/ 
web_1       |            by Mauricio Velazco (@mvelazco)
...
web_1    | [2018-09-02 19:33:43 +0000] [1] [INFO] Starting gunicorn 19.9.0
web_1    | [2018-09-02 19:33:43 +0000] [1] [INFO] Listening at: http://0.0.0.0:8000 (1)
web_1    | [2018-09-02 19:33:43 +0000] [1] [INFO] Using worker: sync
web_1    | [2018-09-02 19:33:43 +0000] [16] [INFO] Booting worker with pid: 16
```

And now you can view Oriana at `http://127.0.0.1:8000`

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

### Loading Data

For the loading and running analytics inside of the docker containers, we can use the `docker-compose` command. Since we have mounted /opt/oriana/data/ to both the container and created it locally on the docker host, we are able to ingest any data which we put into that folder without having to move it into the running container manually. 

*You could setup a Samba share to point to this folder, or run Python WebDAV as a destination from GetEvents.ps1.*

```commandline
docker-compose run web python oriana.py -A load -d /opt/oriana/data
```
 
 ### Run Analytics

 ```
docker-compose run web python oriana.py -A analytics
```
Analytics details will be added to the Wiki.

Happy Hunting !

## Authors

* **Mauricio Velazco** - [@mvelazco](https://twitter.com/mvelazco)

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details

## Docker Overview

Docker configuration explained

- nginx with configuration supplied from config/nginx.conf
- postgres database, which has the configuration settings in docker-compose.yaml and settings.py
- gunicorn to serve the django backend

#### nginx

We mount _/static_ as _/static_ via the docker-compose.yaml and serve /static/ on nginx, while having it proxy the requests upstream to the django server. This gives us the ability to serve the files in a production style manner, but also locally to the box. Currently we are setting this using the Django `STATIC_ROOT` in `settings.py`, and then calling `python manage.py collectstatic --noinput` to move Oriana's static files, as long as any libraries required into `/static`.

Configuration for nginx is in `config/nginx.conf`

#### web

This is the Django application running inside a Python:2.7 image. You can change the configuration of PostgresSQL here, but remember to fix the settings in `settings.py`

If you are running on Windows it is *slightly* untested, but we believe that changing the Oriana data mount path in `docker-compose.yaml` to a local path such as `./data:/opt/oriana/data` should do the trick.

#### PostgresSQL

Database backend for Oriana, configuration of the server is in `docker-compose.yaml` and `settings.py`
