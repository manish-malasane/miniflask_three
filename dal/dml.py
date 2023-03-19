from dal.db_conn_helper import conn_toml
from typing import List
import pydantic
from pymysql import IntegrityError


def insert_resource(
    table_name: str, primary_key: str, primary_value: int, columns: List, values: List
):
    column_names = ", ".join(columns)

    try:
        value_fields = ", ".join(values)
    except (pydantic.error_wrappers.ValidationError, TypeError) as ex:
        print(f"[ ERROR ] - None type values not allowed specify `str`-> {ex}")

    value_fields = ""

    for value in values:
        if isinstance(value, str):
            value_fields = value_fields + '''"''' + value + '''"''' + ""","""
        elif isinstance(value, int):
            value_fields = value_fields + str(value) + ""","""
        else:
            value_fields = value_fields + "Null" + ""","""

    value_fields = value_fields.rstrip(", ")
    result = None
    with conn_toml() as conn:
        cursor = conn.cursor()
        sql_magic = f"""INSERT INTO starwarsDB.{table_name} ({primary_key}, {column_names}) 
                      VALUES({primary_value}, {value_fields})"""

        try:
            result = cursor.execute(sql_magic)
            conn.commit()
        except IntegrityError as fp:
            print(f"[ ERROR ] This data is already stored in database -> {fp}")
    return result


if __name__ == "__main__":
    insert_resource(
        "species",
        "species_id",
        1,
        [
            "name",
            "classification",
            "designation",
            "average_height",
            "skin_colors",
            "hair_colors",
            "eye_colors",
            "average_lifespan",
            "homeworld",
            "language",
        ],
        [
            "Human",
            "mammal",
            "sentient",
            "180",
            "caucasian, black, asian, hispanic",
            "blonde, brown, black, red",
            "brown, blue, green, hazel, grey, amber",
            "120",
            "https://swapi.dev/api/planets/9/",
            "Galactic Basic",
        ],
    )
# """
# DML stands for Data Manipulation Language
# This module contains generic functions to insert data into sql tables
# """
# from dal.db_conn_helper import conn_toml
# from typing import List
#
#
# def insert_resource(
#     table_name: str, primary_key_: str, primary_value: int, columns_: List, values: List
# ):
#     """
#     Inserts a record in the database using primary key
#     Args:
#         table_name (str):
#         primary_key_ (str):
#         primary_value (int):
#         columns_ (list):
#         values (list):
#     Returns:
#         number of records inserted in DB table
#     """
#
#     column_names = ", ".join(columns_)
#     value_fields = ", ".join(values)
#
#     # column_names.rstrip(", ")
#     # value_fields.rstrip(", ")
#
#     value_fields = ""
#     for value in values:
#         if isinstance(value, str):
#             value_fields = value_fields + '''"''' + value + '''"''' + """, """
#         elif isinstance(value, int):
#             value_fields = value_fields + str(value) + ""","""
#
#     value_fields = value_fields.rstrip(""", """)
#     result = None
#     with conn_toml() as conn:
#         cursor = conn.cursor()   # `cursor method`access the connection from conn_toml
#
#         sql_magic = f"""insert into
#         starwarsDB.{table_name} ({primary_key_}, {column_names})
#         values ({primary_value}, {value_fields});"""
#
#         result = cursor.execute(sql_magic)  # .execute access the connection from cursor object& execute the sql_magic
#         conn.commit()  # commits the data for connection
#         breakpoint()
#     return result
#
#
# if __name__ == "__main__":
#     insert_resource("characters", "char_id", 2,
#                     ["name", "height"], ["prashant", "176"])
#
