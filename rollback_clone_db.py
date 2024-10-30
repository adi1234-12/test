#!/usr/bin/env python
import snowflake.connector
from datetime import datetime
import sys
import os

username = os.environ.get("SNOWFLAKE_USER")
password = os.environ.get("SNOWFLAKE_PASSWORD") 
accountname = os.environ.get("SNOWFLAKE_ACCOUNT") 
change_history_table = os.environ.get("CHANGE_HISTORY_TABLE")
database_name = change_history_table.strip().split('.')
#current_date = datetime.now()
#dt_string = current_date.strftime("%d%m%Y")

# Gets the version
ctx = snowflake.connector.connect(
      user= username ,
      password= password,
      account= accountname
      )
cs = ctx.cursor()
version = list()
try:
   #clone Database
   results =cs.execute("CREATE OR REPLACE DATABASE {0}_ROLLBACK_CLONE CLONE {0} ".format(database_name[0]))
   for row in results:
     allRes=results.fetchall()  
finally:
       cs.close()
ctx.close()
