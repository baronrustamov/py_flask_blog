## local debug
execute the following line to set DB_USER DB_ADMIN etc. variables
```. ~/pythonvar.sh```

## pymysql error 1193 Unknown system variable tx_isolation  5161
  * https://github.com/sqlalchemy/sqlalchemy/issues/5161
  * upgrade sqlalchemy and the problem is solved! 1.1.0 -> 1.3.18
