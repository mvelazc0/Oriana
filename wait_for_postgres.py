import os
import logging
from time import time, sleep
import psycopg2

banner = """
________        .__                      
\_____  \_______|__|____    ____ _____   
 /   |   \_  __ \  \__  \  /    \\__  \  
/    |    \  | \/  |/ __ \|   |  \/ __ \_
\_______  /__|  |__(____  /___|  (____  /
        \/              \/     \/     \/ 
"""
banner += "\t\t by Mauricio Velazco (@mvelazco)\n"
banner += "Checking Postgres ---->\n"

print banner

check_timeout = os.getenv("POSTGRES_CHECK_TIMEOUT", 30)
check_interval = os.getenv("POSTGRES_CHECK_INTERVAL", 1)
interval_unit = "second" if check_interval == 1 else "seconds"
config = {
    "dbname": os.getenv("POSTGRES_DB", "oriana"),
    "user": os.getenv("POSTGRES_USER", "oriana"),
    "password": os.getenv("POSTGRES_PASSWORD", "oriana"),
    "host": os.getenv("DATABASE_URL", "postgres"),
}

start_time = time()
logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


def pg_isready(host, user, password, dbname):
    while time() - start_time < check_timeout:
        try:
            conn = psycopg2.connect(**vars())
            logger.info("Postgres is ready for storing Artifacts!")
            conn.close()
            return True
        except psycopg2.OperationalError:
            logger.info("Postgres isn't ready. Waiting for {0} {1}...".format(
                check_interval, interval_unit))
            sleep(check_interval)

    logger.error("We could not connect to Postgres within {0} seconds.".format(
        check_timeout))
    return False


pg_isready(**config)
