import pandas as pd
import requests
import json
import os

class ReverseGeocodingException(Exception):
    pass

class GoogleMapsAPI:

    # google maps api key
    key = 'AIzaSyAeZV95V3hr_3QIgr756MDJNX2v73oC7cs'
    base_url = 'https://maps.googleapis.com/maps/api/geocode/json?'

    def __init__(self, df):
        """Initializes with a pd.DataFrame object."""
        self.df = df
        self.data = pd.DataFrame()

    def reverse_geocoding(self, file='data.json'):
        """Uses the Google Maps API to find a human readable address
        for the latitudes/longitudes pairs in the dataframe.
        Saves information from the API in a JSON file
        named data.json, loads this information inside a pandas DataFrame,
        makes sure it's the most accurate location for the lat/lng pair
        and append in a dataframe that saves information for all lat/lng pairs.
        """
        err = []
        for index, row in self.df.iterrows():
            latlng = str(row['latitude']) + ',' + str(row['longitude'])
            url = self._get_url(latlng)
            response = requests.get(url)
            response = response.json()
            if (response['status'] == 'OK'):
                result = response['results']
                with open(file, 'w') as data:
                    data.write(json.dumps(result, indent=2))

                with open(file, 'r') as data:
                    local_df = json.load(data)
                    local_df = pd.DataFrame(local_df)
                    self.data = self.data.append(local_df.iloc[0]) # -> only the most accurate location
            else:
                err.append([response]) # -> saves an error
        os.remove(file)
        for i in err:
            print(i)
#        file = os.getcwd() + '/processes/data/locations.xlsx'
#        self.data.to_excel(file) # -> only to visualize the dataframe
        return self.data

    def _get_url(self, latlng):
        language = '&language=pt-BR'
        params = f'latlng={latlng}&key={GoogleMapsAPI.key}'
        url = f'{GoogleMapsAPI.base_url}{params}{language}'
        return url
