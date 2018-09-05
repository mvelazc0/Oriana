import argparse
import sys
import os
import django
from utils.analytics import runall
from utils.load_data import load_data
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import getpass
from django.core.management import call_command
from django.core.wsgi import get_wsgi_application

banner="""
________        .__                      
\_____  \_______|__|____    ____ _____   
 /   |   \_  __ \  \__  \  /    \\__  \  
/    |    \  | \/  |/ __ \|   |  \/ __ \_
\_______  /__|  |__(____  /___|  (____  /
        \/              \/     \/     \/ 
"""
banner+="\t\t by Mauricio Velazco (@mvelazco)\n"

if __name__ == '__main__':

    print banner

    parser = argparse.ArgumentParser(usage='oriana.py -A [action] OPTIONS')
    parser.add_argument("-A", "--action", dest="action", nargs='+', default=False, type=str,help="specify the action name: createdb, startdb, load, analytics, runserver")
    parser.add_argument("-d",dest="path", nargs='+', default=False, type=str,help="specify the path of the folder")

    if len(sys.argv)==1:
        parser.print_help()
        print '\n'
        print 'Guide:'
        print 'oriana.py -A createdb              - Create the oriana database and update the django configuration file'
        print 'oriana.py -A startdb               - Create the database schema'
        print 'oriana.py -A load -d [folder path] - Read and index the CSV files found on folder_path'
        print 'oriana.py -A analytics             - Run Orianas analytics'
        print 'oriana.py -A runserver             - Run the web server'
        print 'Hunt !'
        sys.exit(1)

    args = parser.parse_args()

    if args.action[0] == "load":

        if args.path:
            load_data(args.path[0])
        else:
            print "\t[!] The path argument is missing"


    elif args.action[0] == "runserver":

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LM_Hunting.settings")
        #application = get_wsgi_application()
        call_command('runserver', interactive=False)

    elif args.action[0] == "createdb":

        print '\n'
        user = raw_input("Postgres Username:")
        passwd = getpass.getpass("Postgres Password:")

        try:
            con = psycopg2.connect(dbname='', user=user, host='localhost', password=passwd)
            con.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
            cur = con.cursor()
            # cur.execute("DROP DATABASE oriana;")
            cur.execute("CREATE DATABASE oriana;")
            print '\n'
            print "\t[+] Database 'oriana' created"

            try:
                proj_path = os.path.dirname(os.getcwd())
                os.chdir(os.path.join(os.getcwd(), 'LM_Hunting'))
                file = open('settings.py', 'r')
                lines = file.readlines()
                lines[57] = "\t    'USER': '" + user + "',\n"
                lines[58]="\t    'PASSWORD': '"+passwd+"',\n"
                out = open('settings.py', 'w')
                out.writelines(lines)
                out.close()
                print ""
                print "\t[+] Warning: The file",os.path.join(os.getcwd(), 'LM_Hunting','settings.py')+ " has been updated with the cleartext password. "

            except Exception,e:
                print '\n'
                print "File Error: Cannot write to settings.py"
                print e

        except Exception,e:
            print '\n'
            print "Database Error: Check that postgres is running && credentials are valid && permissions are correct."
            print e

    elif args.action[0] == "startdb":

        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LM_Hunting.settings")
        django.setup()
        from django.core.management import call_command
        call_command("migrate", interactive=False)

    elif args.action[0] == "analytics":
        runall()

    elif args.action[0] == "createadmin":
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "LM_Hunting.settings")
        django.setup()
        from django.core.management import call_command
        call_command("createsuperuser", interactive=True)

    sys.exit(1)