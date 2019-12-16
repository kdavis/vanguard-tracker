import os
import time
import sys
import pymysql
from time import strftime
from vanguard import Vanguard

EMAIL = os.environ.get('VANGUARD_USERNAME')
PASSWORD = os.environ.get('VANGUARD_PASSWORD')
HOURS = int(os.environ.get('HOURS'))
DB_HOST = os.environ.get('DB_HOST')
DB_USERNAME = os.environ.get('DB_USERNAME')
DB_PORT = int(os.environ.get('DB_PORT'))
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_DATABASE = os.environ.get('DB_DATABASE')

if EMAIL is None or PASSWORD is None or HOURS is None or DB_HOST is None:
    print("Environment variables are needed!")
    sys.exit(0)

db_create_query = """
CREATE TABLE IF NOT EXISTS vanguard_investments (
    Id INT AUTO_INCREMENT,
    Name VARCHAR(255) NOT NULL,
    Value DECIMAL(18,2) NOT NULL,
    RecordDateTime DATETIME NOT NULL,
    PRIMARY KEY (Id)
)
"""


def execute_query(query):
    conn = pymysql.connect(host=DB_HOST, port=DB_PORT,
                           user=DB_USERNAME, passwd=DB_PASSWORD, db=DB_DATABASE)
    cur = conn.cursor()

    cur.execute(query)

    cur.close()
    conn.commit()
    conn.close()


execute_query(db_create_query)

print("Created database")

while True:
    vanguard = Vanguard(EMAIL, PASSWORD)
    vanguard.login()

    values = vanguard.get_data()
    for value in values:
        print("Found value of %s for %s" % (value['value'], value['name']))

        insert_query = "INSERT INTO vanguard_investments (Name, Value, RecordDateTime) values ('%s', %s, '%s')" % (
            value['name'], value['value'], strftime("%Y-%m-%d %H:%M:%S"))

        execute_query(insert_query)

    print("Inserted data points.")
    time.sleep(HOURS * 3600)
