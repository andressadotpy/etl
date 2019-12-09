import unittest
import os
import pandas as pd
import numpy as np

from ..file_transformation import FileTransformer
from ..maps_api import GoogleMapsAPI
from ..data_transformation import DataTransformation


class TestDataTransformation(unittest.TestCase):

    def setUp(self):
        file = os.getcwd() + '/processes/tests/data_points.txt'
        file_transformation = FileTransformer()
        self.df = file_transformation.transform_data(file)
        self.api = GoogleMapsAPI(self.df)
        self.locations = self.api.reverse_geocoding()
        self.DT = DataTransformation(self.locations)

    def test_assert_dirty_locations_is_pandas_dataframe(self):
        self.assertIsInstance(self.locations, pd.DataFrame)

    def test_assert_dropped_columns_at_init(self):
        self.assertEqual(len(self.DT.df.columns), 2)

    def test_assert_number_of_rows_after_transforming(self):
        latlng = self.DT.lat_lng()
        self.assertEqual(len(latlng), 7)

    def test_assert_number_of_columns_after_transforming(self):
        latlng = self.DT.lat_lng()
        self.assertEqual(len(latlng.columns), 2)

    def test_if_address_components_changes_columns(self):
        df = self.DT.address_components()
        self.assertEqual(len(df.columns), 7)

    def test_concatenate_coordinates_and_addresses_infos(self):
        latlng = self.DT.lat_lng()
        df = self.DT.address_components()
        final_df = self.DT._concatenate_coordinates_and_addresses_infos(latlng)
        self.assertEqual(len(final_df.columns), 9)

    def test_reorganize_columns(self):
        columns = ['latitude', 'longitude', 'rua', 'numero', 'bairro', 'cidade', 'cep', 'estado', 'pais']
        latlng = self.DT.lat_lng()
        df = self.DT.address_components()
        final_df = self.DT._concatenate_coordinates_and_addresses_infos(latlng)
        final_df = self.DT._reorganize_columns()
        self.assertTrue([final_df.columns.values], columns)

    def test_run_all_processes(self):
        columns = ['latitude', 'longitude', 'rua', 'numero', 'bairro', 'cidade', 'cep', 'estado', 'pais']
        df = self.DT.run()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df.columns), 9)
        self.assertTrue([df.columns.values], columns)
