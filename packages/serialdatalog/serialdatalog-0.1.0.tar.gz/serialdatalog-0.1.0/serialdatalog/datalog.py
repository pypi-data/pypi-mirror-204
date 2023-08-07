"""Logging functions for data logger"""
#! /usr/bin/env python

# Python imports
import os
from ast import literal_eval as liteval
import serial
import sqlite3
import logging
from datetime import datetime

# Console logger
clogger = logging.getLogger(__name__)
def logger(
        table_dict,
        source="/dev/ttyACM0",
        dest="datalog.sqlite3",
        encoding='utf-8',
        timeout=10
    ):
    """Logs serial readings

    Args:
        table_dict (dict) : A dictionary containing the "table header" : "data type".
        source (string, optional) : Source port of the serial device.
            Defaults to "/dev/ttyACM0".
        dest (string, optional) : Destination database to write serial output to.
            Defaults to 'datalog.db'
        encoding (string, optional) : Encoding of serial device. 
            Defaults to 'utf-8'.
        timeout (float, optional) : Timeout for reading from the serial port.
            Defaults to 10.

    Returns:
        return val (bool) : True if successful. False otherwise.
    """

    # Connects to source
    with serial.Serial(source, timeout=timeout) as ser:
        clogger.info(f"Connected to:\n{ser}")

        # Connects to database
        con = connect_to_database(dest)
        table_dict["Time_Stamp"] = "REAL"
        table_name = create_database(con, table_dict)

        # Loops over reading serial input
        with open(dest, "a") as f:
            while True:
                try:
                    line = ser.readline().decode(encoding)
                    clogger.info(line)
                    line = line.rstrip().split(",")
                    line.append(datetime.now().strftime('%y%m%d%H%M%S'))
                    data_dict = {
                        h : liteval(line[i]) for i, h in enumerate(list(table_dict.keys()))
                    }
                    add_to_database(con, data_dict, table_name)
                except IndexError:
                    print("Index Error")
                    pass
                except UnicodeDecodeError:
                    print("UnicodeDecodeError")
                    pass
                except KeyboardInterrupt:
                    break
    clogger.info("Finished reading data.")
    return True

def connect_to_database(database):
    """Connects to the SQLite database.

    Args:
        database (str) : The path to the SQLite database.

    Returns:
        sqlite_connection (database connection) : SQLite database connection.
    """

    clogger.debug(f"Trying to connect to {database}...\n")

    sqlite_connection = sqlite3.connect(database)
    cursor = sqlite_connection.cursor()
    version_query = "select sqlite_version()"
    cursor.execute(version_query)
    version_record = cursor.fetchall()
    clogger.info(
        f"Connected to {database}!\n" f"SQLite Database Version is: {version_record}\n"
    )
    cursor.close()
    return sqlite_connection

def create_database(
    connection,
    table_dict,
    table_name=None,
    index=False,
):
    """Adds an empty table for images to a database connection

    Args:
        connection (database connection) : SQLite database connection.
        table_dict (dict) : A dictionary containing the "table header" : "data type".
        table_name (str, optional) : The name for the images table.
            Defaults to the current datetime.        
        index (bool, optional) : Whether to create a unique index for each entry.
            Defaults to True.

    Returns
        return value (bool) : True if successful, False otherwise.
    """

    if table_name is None:
        table_name = f"t{datetime.now().strftime('%Y%m%d%H%M%S')}"

    # Statement to create the image table.
    create_statement = "CREATE TABLE\n" f"{str(table_name)}("
    for key in list(table_dict.keys()):
        create_statement += f"{key} {table_dict[key]},"
    if index:
        create_statement += "PRIMARY KEY('rowid' AUTOINCREMENT),"
    create_statement = create_statement[:-1] + ")"

    # Creates the image table
    connection.execute(create_statement)
    connection.commit()

    return table_name

def add_to_database(connection, data_dict, table_name):
    """Adds image and extracted metadata to database

    Args:
        connection (database connection) : SQLite database connection.
        data_dict (dict) : A dictionary containing the data to add.
        table_name (str) : The table name for the images.
            Defaults to 'model_stats'.

    Returns:
        index (int) : Index of the row entry.
    """

    headers = tuple(data_dict.keys())

    # Converts the data entries into a single row entry.
    row_entry = list(data_dict.values())

    # Insert row query
    insert_query = f"INSERT INTO {table_name}\n" f"{headers} VALUES ("
    insert_query += (len(row_entry) - 1) * "?, " 
    insert_query += "?)"

    # Commits row to database
    cursor = connection.cursor()
    clogger.debug(row_entry)
    cursor.execute(insert_query, row_entry)
    connection.commit()
    rowid = cursor.lastrowid
    cursor.close()

    return rowid

if __name__ == "__main__":
    table_dict = {
        "Elapsed_Time" : "REAL",
        "Finger_Pressure" : "REAL",
        "Height" : "REAL",
        "Arm_Pressure" : "REAL",
        "Finger_Plethysmogram" : "REAL",
    }
    logger(table_dict)
