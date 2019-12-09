import unittest
import os
import pandas as pd

from ..file_transformation import FileTransformer

class TestFileTransformer(unittest.TestCase):

    filepath = os.getcwd()
    filename = filepath + '/processes/tests/data_points.txt'

    def setUp(self):
        self.transformation = FileTransformer()
        self.df = self.transformation.transform_data(TestFileTransformer.filename)

    def test_initialized_not_empty_pandas_DataFrame(self):
        # the DataFrame is not empty because in the setUp TestCase
        # the transform_data already put info inside
        self.assertFalse(self.transformation.coordinates.empty)

    def test_transform_data_returning_pandas_DataFrame(self):
        self.assertIsInstance(self.df, pd.DataFrame)

    def test_DataFrame_returning_correct_number_of_lat_long_pairs(self):
        self.assertEqual(len(self.transformation.coordinates.index), 7)

    def test_DataFrame_returning_lat_long_pairs_for_big_amount_of_data(self):
        filename = TestFileTransformer.filepath + '/processes/data/data_points_20180101.txt'
        df = self.transformation.transform_data(filename)
        self.assertEqual(len(self.transformation.coordinates.index), 998)

    def test_concatenate_pandas_DataFrames(self):
        filename_2 = TestFileTransformer.filepath + '/processes/tests/data_points_2.txt'
        df2 = self.transformation.transform_data(filename_2)
        self.assertEqual(len(self.transformation.coordinates.index), 14)

    def test_concatenate_pandas_DataFrames_big_amount_of_data(self):
        filename_2 = TestFileTransformer.filepath + '/processes/data/data_points_20180101.txt'
        filename_3 = TestFileTransformer.filepath + '/processes/data/data_points_20180102.txt'
        df2 = self.transformation.transform_data(filename_2)
        df3 = self.transformation.transform_data(filename_3)
        self.assertEqual(len(self.transformation.coordinates), 1996)

    def tearDown(self):
        self.transformation.coordinates = pd.DataFrame()
