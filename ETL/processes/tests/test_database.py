import unittest
import unittest.mock
import mysql.connector
import pandas as pd
from ..database import MySQL

class TestDatabase(unittest.TestCase):

    data = {
            'latitude': '-30.049917',
            'longitude': '-51.201439',
            'rua': 'Rua Monsenhor Veras',
            'numero': '405',
            'bairro': 'Santana',
            'cidade': 'Porto Alegre',
            'cep': '90610-010',
            'estado': 'RS',
            'pais': 'Brasil'
            }

    def setUp(self):
        self.db = MySQL()
        self.df = pd.DataFrame(TestDatabase.data, index=[0])

    def test_connection(self):
        self.assertTrue(self.db.cnx)

    def testing_cursos_is_being_created_at_init(self):
        self.assertIsInstance(self.db.cursor,
                                mysql.connector.cursor.MySQLCursor)

    def testing_all_processes(self):
        self.db.sql_processes(self.df)
