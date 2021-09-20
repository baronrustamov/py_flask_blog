import os
import sqlalchemy

RDS_HOSTNAME = os.getenv("RDS_HOSTNAME")
RDS_USERNAME = os.getenv("RDS_USERNAME")
RDS_PASSWORD = os.getenv("RDS_PASSWORD")
RDS_PORT = os.getenv("RDS_PORT")
RDS_DB_NAME = os.getenv("RDS_DB_NAME")

class mysqldb_shell():
  def __init__(self):
    self.db = None

  def init_tcp_connection_engine(db_config):
      # print('init_tcp_connection_engine: ', db_config)
      # [START cloud_sql_mysql_sqlalchemy_create_tcp]
      # Remember - storing secrets in plaintext is potentially unsafe. Consider using
      # something like https://cloud.google.com/secret-manager/docs/overview to help keep
      # secrets secret.
      db_user = os.environ["DB_USER"]
      db_pass = os.environ["DB_PASS"]
      db_name = os.environ["DB_NAME"]
      db_host = os.environ["DB_HOST"]

      # Extract host and port from db_host
      host_args = db_host.split(":")
      db_hostname, db_port = host_args[0], int(host_args[1])

      url = "mysql+pymysql://" + db_user + ":" + db_pass + "@" + db_host \
            + ":" + str(db_port) + "/" + db_name
      pool = sqlalchemy.create_engine(url
          # Equivalent URL:

          # sqlalchemy.engine.url.URL.create(
          #     drivername="mysql+pymysql",
          #     username=db_user,  # e.g. "my-database-user"
          #     password=db_pass,  # e.g. "my-database-password"
          #     host=db_hostname,  # e.g. "127.0.0.1"
          #     port=db_port,  # e.g. 3306
          #     # database=db_name,  # e.g. "my-database-name"
          # ),
          **db_config
      )
      # [END cloud_sql_mysql_sqlalchemy_create_tcp]

      return pool


  def init_connection_engine(self):
    db_config = {
        # [START cloud_sql_mysql_sqlalchemy_limit]
        # Pool size is the maximum number of permanent connections to keep.
        "pool_size": 5,
        # Temporarily exceeds the set pool_size if no connections are available.
        "max_overflow": 2,
        # The total number of concurrent connections for your application will be
        # a total of pool_size and max_overflow.
        # [END cloud_sql_mysql_sqlalchemy_limit]

        # [START cloud_sql_mysql_sqlalchemy_backoff]
        # SQLAlchemy automatically uses delays between failed connection attempts,
        # but provides no arguments for configuration.
        # [END cloud_sql_mysql_sqlalchemy_backoff]

        # [START cloud_sql_mysql_sqlalchemy_timeout]
        # 'pool_timeout' is the maximum number of seconds to wait when retrieving a
        # new connection from the pool. After the specified amount of time, an
        # exception will be thrown.
        "pool_timeout": 30,  # 30 seconds
        # [END cloud_sql_mysql_sqlalchemy_timeout]

        # [START cloud_sql_mysql_sqlalchemy_lifetime]
        # 'pool_recycle' is the maximum number of seconds a connection can persist.
        # Connections that live longer than the specified amount of time will be
        # reestablished
        "pool_recycle": 1800,  # 30 minutes
        # [END cloud_sql_mysql_sqlalchemy_lifetime]
    }

    print('init_connection_engine, os.environ["DB_HOST"]: ', os.environ.get("DB_HOST"))

    if os.environ.get("DB_HOST"):
        return mysqldb_shell.init_tcp_connection_engine(db_config)
      # else:
      #     return init_unix_connection_engine(db_config)

#   def getDances(self):
#       dances = []
#       db = self.db or self.init_connection_engine()
#       with db.connect() as conn:
#           dances = conn.execute(
#               """CREATE DATABASE IF NOT EXISTS pachinko;"""
#           )
#           dances = conn.execute(
#               """USE pachinko;"""
#           )
#           dances = conn.execute(
#               """DROP TABLE dance;"""
#           )
#           dances = conn.execute(
#               "CREATE TABLE IF NOT EXISTS dance "
#               "(dance_id SERIAL NOT NULL, "
#               "dance_style CHAR(30) NOT NULL, PRIMARY KEY (dance_id) );"
#           )
#           dances = conn.execute(
#               "INSERT INTO dance (dance_id, dance_style) VALUES (1, 'swing');"
#           )
#           dances = conn.execute(
#               "INSERT INTO dance (dance_id, dance_style) VALUES (2, 'salsa');"
#           )
#           dances = conn.execute(
#               """SELECT * FROM dance;"""
#           )

#       # Convert it into a list for readability
#       dances = [list(l) for l in dances]
#       print('get Dances from mysql DB: ', dances)
#       return dances

