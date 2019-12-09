import os

from processes.file_transformation import FileTransformer
from processes.maps_api import GoogleMapsAPI
from processes.data_transformation import DataTransformation

if __name__ == '__main__':
    path = os.getcwd() + '/processes/data/'
    files = [
            'data_points_20180101.txt',
            'data_points_20180102.txt',
            'data_points_20180103.txt'
            ]
    T = FileTransformer()
    for file in files:
        data = T.transform_data(path + file)
    coordinates = T.get_lat_lng_pairs()
    maps_api = GoogleMapsAPI(coordinates)
    messy_data = maps_api.reverse_geocoding()
    df = DataTransformation(messy_data)
    df = df.run()
    file = 'df.xlsx'
    df.to_excel(path+file)
