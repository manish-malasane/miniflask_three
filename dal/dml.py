import logging

import pymysql
from dal.db_conn_helper import conn_toml
from typing import List, Union, Dict
import pydantic
from pymysql import IntegrityError
import requests
from collections import OrderedDict


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


def get_url(resource, resource_id) -> str:
    home_url = "https://swapi.dev"
    relative_url = f"/api/{resource}/{resource_id}"
    absolute_url = home_url + relative_url
    return absolute_url


def fetch_resource(resource):
    home_url = "https://swapi.dev"
    relative_url = f"/api/{resource}"
    absolute_url = home_url + relative_url
    response = requests.get(absolute_url)
    data = response.json()
    return data


def __delete_resource(
    table_name: str, primary_key: str, primary_value: Union[int, str]
):
    try:
        with conn_toml() as conn:
            cursor = conn.cursor()
            sql_magic = f"DELETE FROM {table_name} WHERE {primary_key}={primary_value}"
            data = cursor.execute(sql_magic)
            conn.commit()

        return data
    except pymysql.Error as ex:
        return f" [ ERROR DETAILS ] :-> {ex}"


def build_upsert_sql_query(
    table_name, command, prime_key, prime_value, clause, keys_, values_
):
    """BUilds sql query based on input.
    Args:
        table_name (str): table under consideration for sql query.
        command (str): sql commands such as select, insert, update etc.
        prime_key (str): primary key for particular table.
        prime_value(int, str): value to be updated for primary key
        clause (str): clauses to filter results.
        keys_ (list): list of keys query refers to.
        values_ (list): list of values query stores (required for insert and update statements.)
    Returns:
        query (str): complete sql query
    """

    if prime_key in keys_:
        keys_.remove(prime_key)

    key_literals = ", ".join(keys_)

    mid_literals = []

    if int(prime_value) in values_:
        values_.remove(int(prime_value))

    for i in range(len(values_)):
        mid = '''"''' + str(values_[i]) + '''"'''
        mid_literals.append(mid)

    value_literals = ", ".join(mid_literals)

    mid_update_literals = []

    for key_lit, val_lit in zip(keys_, mid_literals):
        mid = """ , """ + key_lit + """=""" + val_lit
        mid_update_literals.append(mid)

    update_literals = "".join(mid_update_literals)

    update_literals = update_literals[3:]

    sql = f"""{command} {table_name} 
          ({prime_key}, {key_literals}) 
          VALUES ({int(prime_value)}, {value_literals})
          {clause} {update_literals};"""

    return sql


def get_url_ids(urls) -> str:
    """retrieves id part of singular record urls such as -
     `https://swapi.co/api/characters/2/`
    Args:
        urls (list): list of urls
    Returns:
        str: space delimited string having ids from all urls.
    """

    ids = []

    for url in urls:
        ids.append(url.split("/")[-1])

    return " ".join(ids)


def upsert_films(film: Dict, endpoint: str):
    """
    NOTE:-
        upsert = update + insert
        "swapi.dev/api/films/1
    Inserts values into `films` table, updates on duplicate key.
    Args:
        film (dict):
        endpoint (str):
    Returns:
    """

    connection = conn_toml()
    film = OrderedDict(film)
    film_id = int(get_url_ids([endpoint]))

    keys_ = []
    values_ = []

    for key, val in film.items():
        keys_.append(key)
        if isinstance(val, list):
            values_.append(get_url_ids(val))
        else:
            values_.append(val)

    # Here we are importing some modules inside the func to avoid circular imports
    from models.datamodels.films import Films
    from pydantic.error_wrappers import ValidationError

    try:
        if film is not OrderedDict([("Details", "Not Found")]):
            Films(**film)
        else:
            print(f"[ WARNING ] Endpoint - {endpoint} - yields nothing!!")
            return None
    except ValidationError as ex:
        print(
            f"""[ Error ] fetched film record does not meet validations.
            Perhaps, type conversions required. More details on error  - {ex}"""
        )

    try:
        with connection.cursor() as cursor:
            sql_magic = build_upsert_sql_query(
                "film",
                "INSERT INTO",
                "film_id",
                film_id,
                "ON DUPLICATE KEY UPDATE",
                keys_,
                values_,
            )
            result = cursor.execute(sql_magic)
            connection.commit()
    except pymysql.Error as ex:
        logging.error(f"ERROR DETAILS :- {ex}")
        return 0
    finally:
        connection.close()

    return result


def upsert_characters(character: Dict, endpoint: str):
    """
    NOTE:-
        upsert = update + insert
        "swapi.dev/api/films/1
    Inserts values into `films` table, updates on duplicate key.
    Args:
        character (dict):
        endpoint (str):
    Returns:
    """

    connection = conn_toml()
    character = OrderedDict(character)
    char_id = int(get_url_ids([endpoint]))

    keys_ = []
    values_ = []

    for key, val in character.items():
        keys_.append(key)
        if isinstance(val, list):
            values_.append(get_url_ids(val))
        else:
            values_.append(val)

    # Here we are importing some modules inside the func to avoid circular imports
    from models.datamodels.characters import Characters
    from pydantic.error_wrappers import ValidationError

    try:
        if character is not OrderedDict([("Details", "Not Found")]):
            Characters(**character)
        else:
            print(f"[ WARNING ] Endpoint - {endpoint} - yields nothing!!")
            return None
    except ValidationError as ex:
        print(
            f"""[ Error ] fetched film record does not meet validations.
            Perhaps, type conversions required. More details on error  - {ex}"""
        )

    try:
        with connection.cursor() as cursor:
            sql_magic = build_upsert_sql_query(
                "characters",
                "INSERT INTO",
                "char_id",
                char_id,
                "ON DUPLICATE KEY UPDATE",
                keys_,
                values_,
            )
            result = cursor.execute(sql_magic)
            connection.commit()
    except pymysql.Error as ex:
        logging.error(f"ERROR DETAILS :- {ex}")
        return 0
    finally:
        connection.close()

    return result


def upsert_planets(planet: Dict, endpoint: str):
    """
    NOTE:-
        upsert = update + insert
        "swapi.dev/api/films/1
    Inserts values into `films` table, updates on duplicate key.
    Args:
        planet (dict):
        endpoint (str):
    Returns:
    """

    connection = conn_toml()
    planet = OrderedDict(planet)
    planet_id = int(get_url_ids([endpoint]))

    keys_ = []
    values_ = []

    for key, val in planet.items():
        keys_.append(key)
        if isinstance(val, list):
            values_.append(get_url_ids(val))
        else:
            values_.append(val)

    # Here we are importing some modules inside the func to avoid circular imports
    from models.datamodels.planets import Planets
    from pydantic.error_wrappers import ValidationError

    try:
        if planet is not OrderedDict([("Details", "Not Found")]):
            Planets(**planet)
        else:
            print(f"[ WARNING ] Endpoint - {endpoint} - yields nothing!!")
            return None
    except ValidationError as ex:
        print(
            f"""[ Error ] fetched film record does not meet validations.
            Perhaps, type conversions required. More details on error  - {ex}"""
        )

    try:
        with connection.cursor() as cursor:
            sql_magic = build_upsert_sql_query(
                "planet",
                "INSERT INTO",
                "planet_id",
                planet_id,
                "ON DUPLICATE KEY UPDATE",
                keys_,
                values_,
            )
            result = cursor.execute(sql_magic)
            connection.commit()
    except pymysql.Error as ex:
        logging.error(f"ERROR DETAILS :- {ex}")
        return 0
    finally:
        connection.close()

    return result


def upsert_species(specie: Dict, endpoint: str):
    """
    NOTE:-
        upsert = update + insert
        "swapi.dev/api/films/1
    Inserts values into `films` table, updates on duplicate key.
    Args:
        specie (dict):
        endpoint (str):
    Returns:
    """

    connection = conn_toml()
    specie = OrderedDict(specie)
    specie_id = int(get_url_ids([endpoint]))

    keys_ = []
    values_ = []

    for key, val in specie.items():
        keys_.append(key)
        if isinstance(val, list):
            values_.append(get_url_ids(val))
        else:
            values_.append(val)

    # Here we are importing some modules inside the func to avoid circular imports
    from models.datamodels.species import Species
    from pydantic.error_wrappers import ValidationError

    try:
        if specie is not OrderedDict([("Details", "Not Found")]):
            Species(**specie)
        else:
            print(f"[ WARNING ] Endpoint - {endpoint} - yields nothing!!")
            return None
    except ValidationError as ex:
        print(
            f"""[ Error ] fetched film record does not meet validations.
            Perhaps, type conversions required. More details on error  - {ex}"""
        )

    try:
        with connection.cursor() as cursor:
            sql_magic = build_upsert_sql_query(
                "species",
                "INSERT INTO",
                "species_id",
                specie_id,
                "ON DUPLICATE KEY UPDATE",
                keys_,
                values_,
            )
            result = cursor.execute(sql_magic)
            connection.commit()
    except pymysql.Error as ex:
        logging.error(f"ERROR DETAILS :- {ex}")
        return 0
    finally:
        connection.close()

    return result


def upsert_vehicles(vehicle: Dict, endpoint: str):
    """
    NOTE:-
        upsert = update + insert
        "swapi.dev/api/films/1
    Inserts values into `films` table, updates on duplicate key.
    Args:
        vehicle (dict):
        endpoint (str):
    Returns:
    """

    connection = conn_toml()
    vehicle = OrderedDict(vehicle)
    vehicle_id = int(get_url_ids([endpoint]))

    keys_ = []
    values_ = []

    for key, val in vehicle.items():
        keys_.append(key)
        if isinstance(val, list):
            values_.append(get_url_ids(val))
        else:
            values_.append(val)

    # Here we are importing some modules inside the func to avoid circular imports
    from models.datamodels.vehicles import Vehicles
    from pydantic.error_wrappers import ValidationError

    try:
        if vehicle is not OrderedDict([("Details", "Not Found")]):
            Vehicles(**vehicle)
        else:
            print(f"[ WARNING ] Endpoint - {endpoint} - yields nothing!!")
            return None
    except ValidationError as ex:
        print(
            f"""[ Error ] fetched film record does not meet validations.
            Perhaps, type conversions required. More details on error  - {ex}"""
        )

    try:
        with connection.cursor() as cursor:
            sql_magic = build_upsert_sql_query(
                "vehicle",
                "INSERT INTO",
                "vehicle_id",
                vehicle_id,
                "ON DUPLICATE KEY UPDATE",
                keys_,
                values_,
            )
            result = cursor.execute(sql_magic)
            connection.commit()
    except pymysql.Error as ex:
        logging.error(f"ERROR DETAILS :- {ex}")
        return 0
    finally:
        connection.close()

    return result


def upsert_starships(starship: Dict, endpoint: str):
    """
    NOTE:-
        upsert = update + insert
        "swapi.dev/api/films/1
    Inserts values into `films` table, updates on duplicate key.
    Args:
        starship (dict):
        endpoint (str):
    Returns:
    """

    connection = conn_toml()
    starship = OrderedDict(starship)
    starship_id = int(get_url_ids([endpoint]))

    keys_ = []
    values_ = []

    for key, val in starship.items():
        keys_.append(key)
        if isinstance(val, list):
            values_.append(get_url_ids(val))
        else:
            values_.append(val)

    # Here we are importing some modules inside the func to avoid circular imports
    from models.datamodels.starships import Starships
    from pydantic.error_wrappers import ValidationError

    try:
        if starship is not OrderedDict([("Details", "Not Found")]):
            Starships(**starship)
        else:
            print(f"[ WARNING ] Endpoint - {endpoint} - yields nothing!!")
            return None
    except ValidationError as ex:
        print(
            f"""[ Error ] fetched film record does not meet validations.
            Perhaps, type conversions required. More details on error  - {ex}"""
        )

    try:
        with connection.cursor() as cursor:
            sql_magic = build_upsert_sql_query(
                "starship",
                "INSERT INTO",
                "starship_id",
                starship_id,
                "ON DUPLICATE KEY UPDATE",
                keys_,
                values_,
            )
            result = cursor.execute(sql_magic)
            connection.commit()
    except pymysql.Error as ex:
        logging.error(f"ERROR DETAILS :- {ex}")
        return 0
    finally:
        connection.close()

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
