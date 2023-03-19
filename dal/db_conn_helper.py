"""
1. create a package called `dal` at project root
2. create a sub-package under `dal` package named `settings`
3. create a config file named `secrets.yaml` and copy-paste following code

https://paste.centos.org/view/a3746a77

4. create a python file under `dal` named `db_conn_helper.py`
   and copy-paste following code.

   https://paste.centos.org/view/c6f75a2d


5. execute `db_conn_helper.py` from the "run" button available at entrypoint clause.
"""
import toml
import pymysql
import yaml


def conn_toml():
    try:
        with open("dal/settings/secrets.toml", "r") as fp:
            resource = toml.load(fp)
            config = resource.get("mysqldb")
            conn = pymysql.connect(**config)
            return conn
    except pymysql.err.Error as ex:
        print(f"[ ERROR ] cannot establish connection -{ex}")


def conn_yaml():
    try:
        with open("settings/secrets.yaml", "r") as fp:
            resource = yaml.load(fp, Loader=yaml.FullLoader)
            config = resource.get("db")
            conn = pymysql.connect(**config)
            return conn

    except pymysql.err.Error as ex:
        print(f"[ ERROR ] cannot establish connection -{ex}")


if __name__ == "__main__":
    toml_conn = conn_toml()
    print(toml_conn)
    yaml_conn = conn_yaml()
    print(yaml_conn)


"""
Reference CODE :- 1
"""
"""

# This module defines utility to connect with database.
# 
# pip install pymysql
# pip install cryptography
# 
# 
# # if you want to create new user and want to grant to root permissions to him
# 
# CREATE USER adam@localhost IDENTIFIED BY 'qwerty@123';
# GRANT ALL PRIVILEGES ON *.* TO adam WITH GRANT OPTION;
# SHOW GRANTS FOR adam;
# 
# """
#
# import os
# import yaml
# import toml
# import pymysql
# from typing import List
# from pymysql.connections import Connection
#
#
# _settings = {}
#
#
# def _load_from_file(filename):
#     """Loads settings from a YAML file and stores them under the ``_settings``
#     global variable
#     Args:
#         filename (str): The filename of the YAML file containing the settings.
#     """
#
#     global _settings
#
#     if not os.path.exists(filename):
#         return
#
#     with open(filename, "r") as f:
#         doc = yaml.load(f, Loader=yaml.FullLoader)
#
#     if not doc:
#         return
#
#     for k, v in doc.items():
#         _settings[k] = v
#
#
# def _abs_path(filename):
#     """Returns the absolute path to the provided ``filename``.
#     Args:
#         filename (str): The filename for which the absolute path will be
#             assembled.
#     Returns:
#         str: The assembled absolute path for ``filename``.
#     """
#
#     return os.path.join(os.path.dirname(__file__), filename)
#
#
# def _load():
#     """Loads the settings YAML files and stores their content under the
#     ``_settings`` variable.
#     Note:
#         Settings under ``settings/secrets.yaml`` are only loaded in a DEV
#         environment.
#     """
#
#     global _settings
#
#     env_filename = _abs_path("settings/secrets.yaml")
#     _load_from_file(env_filename)
#
#
# def get_db_conn() -> Connection:
#     """Assembles connection object to the SQL database.
#     Returns:
#         Connection:  connection object to the SQL database.
#     """
#
#     _load()
#     global _settings
#
#     sql_username = _settings.get("LOCALSQL_USER")
#     sql_password = _settings.get("LOCALSQL_PASSWORD")
#     sql_host = _settings.get("LOCALSQL_HOST") or ""
#     sql_port = _settings.get("LOCALSQL_PORT")
#     sql_db = _settings.get("LOCALSQL_DATABASE")
#
#     connection = pymysql.connect(
#         host=sql_host,
#         user=sql_username,
#         password=sql_password,
#         db=sql_db,
#         port=sql_port,
#         charset="utf8mb4",
#         cursorclass=pymysql.cursors.DictCursor,
#     )
#
#     return connection
#
#
# def get_db_conn_toml():
#
#     toml_path = "settings/secrets.toml"
#
#     with open(toml_path, "r") as foo:
#         config = toml.load(foo)
#         dbconfig = config.get("mysqldb")
#         connection_ = pymysql.connect(**dbconfig)
#         return connection_
#
#
# if __name__ == "__main__":
#     yaml_conn = get_db_conn()
#     toml_conn = get_db_conn_toml()
"""
References CODE :- 2 
"""
#
# import pymysql
# import toml
# import yaml
#
# from pymysql.connections import Connection
#
# _settings = {}
#
#
# def make_connection():
#     try:
#         connection = pymysql.connect(
#             user="root",
#             password="root@123",
#             host="127.0.0.1",
#             port=3306,
#             database="starwarsDB"
#         )
#         return connection
#     except pymysql.err.Error as ex:
#         print(f"[ ERROR ] cannot establish connection - {ex}")
#
# def _load_from_yaml():

#
#     global _settings
#
#     with open("settings/secrets.yaml", "r") as fp:
#         doc = yaml.load(fp, Loader=yaml.FullLoader)
#
#     if not doc:
#         return
#
#     for key_, val_ in doc.items():
#         _settings[key_] = val_
#
#
# def get_db_conn() -> Connection:

#
#     _load_from_yaml()
#
#     try:
#         connection = pymysql.connect(**_settings)
#         return connection
#     except pymysql.err.Error as ex:
#         print(f"[ ERROR ] cannot make connection {ex}")
#
#
# def get_db_conn_toml():
#     """picks configurations from settings/secret.toml
#
#    {
#    'host': '127.0.0.1',
#    'user': 'root',
#    'port': 3306,
#    'database': 'starwarsDB',
#    'password': 'root@123'
#  }
#  """
#
#     with open("settings/secrets.toml", "r") as fp:
#         config = toml.load(fp)
#         dbconfig = config.get("mysqldb")
#         conn_ = pymysql.connect(**dbconfig)
#         return conn_
#
#
# if __name__ == "__main__":
#     conn = make_connection()
#     toml_conn = get_db_conn_toml()
#     yaml_conn = get_db_conn()
#     breakpoint()
