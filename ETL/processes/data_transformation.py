import os
import pandas as pd
import numpy as np
from functools import reduce


class DataTransformation:

    def __init__(self, df):
        self.df = self._format_df(df)

    def run(self):
        """Run all processes together and returns
        the modified dataframe.
        """
        coordinates = self.lat_lng()
        self.df = self.address_components()
        self.df = self._concatenate_coordinates_and_addresses_infos(coordinates)
        self.df = self._reorganize_columns()
        return self.df

    def lat_lng(self):
        """Creates a coordinates dictionary to save
        latitude/longitude pairs values.
        Returns a pd.DataFrame from dict coordinates.
        """
        coordinates = {'latitude': [], 'longitude':[]}
        for row in range(len(self.df)):
            latitude, longitude = self._get_lat_and_lng(row)
            coordinates['latitude'].append(latitude)
            coordinates['longitude'].append(longitude)
        coordinates = pd.DataFrame(coordinates)
        file = os.getcwd() + '/processes/data/coordinates.xlsx'
        coordinates.to_excel(file) # -> only to visualize the dataframe
        return coordinates

    def address_components(self):
        """Modify in place the initialized df
        and returns the modified df.
        The modified df has 7 columns with

        ['rua', 'numero', 'bairro', 'cidade',
        'cep', 'estado', 'pais']

        Makes sure 'estado' is the abbreviation.
        Ex: 'Rio Grande do Sul' is saved as 'RS'.
        """
        self.df = self._create_item_column()
        self.df = self.df.explode('types')
        self.df = self._change_tags()
        self.df = self.df.drop_duplicates()
        self.df = self.df.dropna()
        self.df.loc[self.df.types == 'estado', 'long_name'] = self.df['short_name']
        item = self.df.item
        self.df = self.df.rename(columns={'types':'Index'})
        self.df = self.df.pivot(columns='Index', values='long_name')
        self.df['item'] = item
        self.df = self.df.fillna('')
        self.df = self.df.groupby(['item']).sum()
        self.df = self.df.replace('', np.nan)
        return self.df

    def reduce_memory_usage(self):
        memory_before = self.df.memory_usage()
        self.df.reset_index(inplace=True)
        self.df = self.df.drop(columns=['item'])
        category = ['bairro', 'cidade', 'estado', 'pais']
        for c in category:
            temp = self.df[c]
            self.df[c] = temp.astype('category')
        memory_after = self.df.memory_usage()
        print('Memory before:', memory_before)
        print('Memory after:', memory_after)

    def _concatenate_coordinates_and_addresses_infos(self, coordinates):
        self.df = pd.concat([self.df, coordinates], axis='columns')
        return self.df

    def _create_item_column(self):
        output = []
        for i, items in enumerate(self.df['address_components']):
            for item in items:
                tmp = item
                tmp['item'] = i
                output.append(tmp)
        output = pd.DataFrame(output)
        return output

    def _change_tags(self):
        """Maps the types of tags from Google Maps API to
        the correct names in portuguese in addr_comp.
        Those types that represents not needed information
        are given the value np.nan."""

        types = ['street_number', 'route', 'establishment',
                'point_of_interest', 'transit_station',
                'sublocality', 'sublocality_level_1',
                'administrative_area_level_2',
                'administrative_area_level_1', 'country',
                'postal_code', 'political', 'park', 'locality', 'subway_station'
                'postal_code_prefix', 'bus_station', 'premise', 'subpremise']

        addr_comp =['numero', 'rua', 'rua', 'rua', 'rua',
                    'bairro', 'bairro', 'cidade', 'estado',
                    'pais', 'cep', np.nan, 'rua', 'cidade', 'rua', np.nan,
                    'rua', np.nan, np.nan]
        mapped_types = dict(zip(types, addr_comp))
        self.df['types'] = self.df['types'].map(mapped_types)
        return self.df

    def _reorganize_columns(self):
        columns = ['latitude', 'longitude', 'rua', 'numero', 'bairro', 'cidade', 'cep', 'estado', 'pais']
        self.df = self.df[columns]
        return self.df

    def _format_df(self, df):
        """Helper method to help prepare df.
        df is a pd.DataFrame that came directly from GoogleMapsAPI.
        Drop columns that aren't used and set index
        of length df.
        Returns a changed df."""
        df = df.drop(columns=[
                            'place_id', 'plus_code',
                            'types', 'formatted_address'])
        df['index'] = range(len(df))
        df = df.set_index(['index'])
        return df

    def _get_lat_and_lng(self, row):
        """Helper method that returns the latitude and longitude
        values for a dataframe row.
        """
        latitude = self._get_from_dict(self.df['geometry'][row],
                                        ['location', 'lat'])
        longitude = self._get_from_dict(self.df['geometry'][row],
                                        ['location', 'lng'])
        return (latitude, longitude)

    def _get_from_dict(self, data_dict, map_list):
        """Helper method to iterate nested dictionary."""
        return reduce(dict.get, map_list, data_dict)
