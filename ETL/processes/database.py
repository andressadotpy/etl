from __future__ import print_function

import mysql.connector
from mysql.connector.errors import Error as err
from mysql.connector import errorcode

import pandas as pd


class MySQL:

    db = 'locations'

    config = {
            'user': 'root',
            'password': '',
            'host': 'localhost',
            'port': 3306,
            }

    table = {}

    table['locations'] = (
        """CREATE TABLE locations (
          latitude VARCHAR(40),
          longitude VARCHAR(40),
          rua VARCHAR(30),
          numero INT,
          bairro VARCHAR(30),
          cidade VARCHAR(255),
          cep VARCHAR(9),
          estado VARCHAR(4),
          pais VARCHAR(25))""")

    def __init__(self):
        """Initialize a MySQL object and connect to a MySQL server."""
        self.cnx = mysql.connector.connect(**MySQL.config)
        self.cursor = self.cnx.cursor()

    def sql_processes(self, df): # -> df is a pandas DataFrame
        """Use MySQL methods to create the database locations,
        if it's not created.
        Creates the table with the correct columns and inserts
        information in that table from a pandas DataFrame.
        """
        self.create_database()
        self.start()
        self.create_table()
        self.insert(df)
        self.end_con()

    def create_database(self):
        try:
            self.cursor.execute(f'CREATE DATABASE IF NOT EXISTS {MySQL.db}')
        except mysql.connector.Error as err:
            print(err)
            exit(1)

    def start(self):
        try:
            self.cursor.execute(f'USE {MySQL.db}')
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                self.create_database()
                print(f'{MySQL.db} was created.')
                cnx.database = MySQL.db
            else:
                print(err)
                exit(1)

    def create_table(self):
        for table_name in MySQL.table:
            table_description = MySQL.table[table_name]
            try:
                print(f'Creating table {table_name}:', end='')
                self.cursor.execute(table_description)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print('Table already exists.')
                else:
                    print(err.msg)
            else:
                print('OK')

    def insert(self, df):
        """Insert pandas dataframe into MySQL database."""
        cols = ",".join([str(i) for i in df.columns.tolist()])
        for i, row in df.iterrows():
            sql = "INSERT INTO locations (" + cols + ") VALUES (" + "%s,"*(len(row)-1) + "%s)"
            self.cursor.execute(sql, tuple(row))
            self.cnx.commit()

    def end_con(self):
        self.cursor.close()
        self.cnx.close()
