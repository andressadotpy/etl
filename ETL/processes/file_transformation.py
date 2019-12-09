import pandas as pd

class FileTransformer:
    """Transform data from .txt files to get better format
    to latitude and longitude information.
    """

    def __init__(self):
        """Initializes the class with an empty pd.DataFrame."""
        self.coordinates = pd.DataFrame()

    def transform_data(self, filename):
        """Receives data from a file in the format:

        Latitude: 30°03′49″S   -30.06355608
        Longitude: 51°13′59″W   -51.2331063
        Distance: 3.5427 km  Bearing: 204.819°

        Returns a pd.DataFrame in the format:


	           latitude 	longitude
        index
        0 	-30.04982864 	-51.20150245
        1 	-30.06761588 	-51.23976111
        2 	-30.05596474 	-51.17286827
        3 	-30.03841576 	-51.24943145

        """
        df = pd.read_fwf(filename, colspecs=[(0,9),(10,21),(21,38)], header=None)
        df = df[~df[0].str.contains('Distance:')]
        df = df.drop(columns=[1])
        df = df.pivot(columns=0, values=2)
        df['Longitude'] = df['Longitude'].bfill()
        df = df.dropna()
        df.columns = ['latitude', 'longitude']
        df['index'] = range(len(df))
        df = df.set_index(['index'])
        self.coordinates = self._concatenate_dataframe(df)
        return df

    def _concatenate_dataframe(self, df):
        self.coordinates = self.coordinates.append(df)
        self.coordinates = self._assert_no_duplicates()
        return self.coordinates

    def _assert_no_duplicates(self):
        self.coordinates = self.coordinates.drop_duplicates()
        return self.coordinates

    def get_lat_lng_pairs(self):
        return self.coordinates
