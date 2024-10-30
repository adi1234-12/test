#!/usr/bin/env python
#*******************************************************************************
# Author:      Sukarnn Taneja
# Create date: 25th Apr''21
# Description: git action cicd snowpydeploy pyhton script to execute SQL Queries on snowflake 
# Parameters: Gets parameters from git action yml file 
# Returns:  Success or Failure 
#
# Change History:
#	By: Nikunj Gada 25th April 2023
#	Notes:	Added parameters for connecting to snowflake using private key. Search for comment added by Nikunj to follow the change
#
# Change History:
#	By: 
#	Notes:	
#********************************************************************************
import snowflake.connector
import sys
import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import dsa
from cryptography.hazmat.primitives import serialization

username = os.environ.get("SNOWFLAKE_USER")
#password = os.environ.get("SNOWFLAKE_PASSWORD") 
accountname = os.environ.get("SNOWFLAKE_ACCOUNT") 
change_history_table = os.environ.get("CHANGE_HISTORY_TABLE")
warehouse = os.environ["SNOWFLAKE_WAREHOUSE"]

table_name_parts = change_history_table.strip().split('.')


'''
with open(os.environ["SNOWFLAKE_PRIVATE_KEY_PATH"], "rb") as key:
    p_key= serialization.load_pem_private_key(
    key.read(),
    password = os.environ['SNOWFLAKE_PRIVATE_KEY_PASSPHRASE'].encode(),
    backend = default_backend()
  )
'''
  
key=bytes(os.environ["SNOWFLAKE_PRIVATE_KEY"], 'utf-8')
p_key= serialization.load_pem_private_key(
key,
password = os.environ['SNOWFLAKE_PRIVATE_KEY_PASSPHRASE'].encode(),
backend = default_backend()
)

pkb = p_key.private_bytes(
    encoding = serialization.Encoding.DER,
    format = serialization.PrivateFormat.PKCS8,
    encryption_algorithm = serialization.NoEncryption())

# Gets the version
ctx = snowflake.connector.connect(
      user= username ,
      private_key = pkb,
      #password= password,
      account= accountname,
      warehouse=warehouse
      )
cs = ctx.cursor()
version = list()
try:
   results = cs.execute("CREATE TABLE IF NOT EXISTS \"{0}\".\"{1}\".CHANGE_HISTORY (VERSION VARCHAR(16777216),DESCRIPTION VARCHAR(16777216),SCRIPT VARCHAR(16777216),SCRIPT_TYPE VARCHAR(16777216),CHECKSUM VARCHAR(16777216),EXECUTION_TIME NUMBER(38,0),STATUS VARCHAR(16777216),ENVIRONMENT VARCHAR(16777216),GIT_REPOSITORY VARCHAR(16777216),GIT_BRANCH VARCHAR(16777216),GIT_COMMIT VARCHAR(16777216),RELEASE_COMMENTS VARCHAR(16777216),INSTALLED_BY VARCHAR(16777216),INSTALLED_ON TIMESTAMP_NTZ(9))".format(table_name_parts[0],table_name_parts[1]))   
   for row in results:
     allRes=results.fetchall()
   resultset=cs.execute("SELECT TO_CHAR(NVL(round(version),0)+1) FROM {0}.\"{1}\".{2} WHERE SCRIPT_TYPE = 'V' ORDER BY INSTALLED_ON DESC LIMIT 1".format(table_name_parts[0], table_name_parts[1], table_name_parts[2]))
   for row in resultset:
      version=row[0]
finally:
       cs.close()
ctx.close()

if len(version) == 0:
      version=1
print(version)
