'''-----------------------SETUP STEPS------------------------------------------------------
Install Psycopg2: 
    pip install psycopg2-binary

Create database on device using the faostat_dump.sql (dump of the database):
    createdb <database_name>
    psql -d <database_name> -f faostat_dump.sql

Configure database.ini:
    copy database.ini.example to a new file called database.ini
    under [postgresql], fill in:
       host      localhost (default)
       database  your database name (default: faostat, change to whatever you used)
       user      your Postgres username
       password  your Postgres password (remove if not needed)
       
NOTE: user, password should be whatever you used from the setup in class. 
Anytime you want to connect to the database make sure the PostgreSQL server is running
on your device.
---------------------------------------------------------------------------------------------'''

import psycopg2
from configparser import ConfigParser

# Configuration Management using database.ini
def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    parser.read(filename)

    config = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params: 
            config[param[0]] = param[1]
    else: 
        raise Exception(f'Section {section} not found in the {filename} file')
    return config

# Use this in the tools methods to get the connection
def get_connection(): 
    conn = psycopg2.connect(**load_config(section='postgresql'))
    conn.set_session(readonly=True, autocommit=True)
    return conn

# Example Usage 
def test(): 
    conn = get_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM item LIMIT 10')
    for item_code, item_name in cur:    # iterate through the tuples
        print(item_code, item_name)
    cur.close()
    conn.close()

# Uncomment to test
# test()