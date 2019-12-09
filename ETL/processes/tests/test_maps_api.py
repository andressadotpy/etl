import unittest
import os
import pandas as pd

from ..maps_api import GoogleMapsAPI
from ..file_transformation import FileTransformer

class TestGoogleMapsAPI(unittest.TestCase):

    def setUp(self):
        self.filepath = os.getcwd()
        self.filename_1 = self.filepath + '/processes/tests/data_points.txt'
        self.filename_2 = self.filepath + '/processes/tests/data_points_2.txt'
        self.T = FileTransformer()
        self.df1 = self.T.transform_data(self.filename_1)
        self.df2 = self.T.transform_data(self.filename_2)
        self.coordinates = self.T.coordinates
#        self.api = GoogleMapsAPI(self.coordinates)

    @unittest.skip
    def test_is_working_google_maps_api_small_amount_data(self):
        result = self.api.reverse_geocoding('test_data.json')
        self.assertIsInstance(result, pd.DataFrame)

    @unittest.skip
    def test_is_working_google_maps_api_with_big_amount_data(self):
        path =  os.getcwd()
        file = path + '/processes/data/data_points_20180101.txt'
        T = FileTransformer()
        df = T.transform_data(file)
        coordinates = T.coordinates
        api = GoogleMapsAPI(coordinates)
        result = api.reverse_geocoding('test_more_data.json')
        self.assertEqual(len(result), 998)
