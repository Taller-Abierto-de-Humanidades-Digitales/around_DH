"""
Module to convert a CSV file to a GeoJSON file.
"""

import pandas as pd
import json
from geojson import Feature, FeatureCollection, Point


class Csv2Geojson:
    """
    Class to convert a CSV file to a GeoJSON file.
    """

    def __init__(self, csv_file, geojson_file):
        """
        Initialize the class.
        """
        self.csv_file = csv_file
        self.geojson_file = geojson_file

    def csv2geojson(self):
        """
        Convert a CSV file to a GeoJSON file.
        """
        df = pd.read_csv(self.csv_file)
        features = df.apply(lambda row: Feature(geometry=Point((row['longitude'], row['latitude']))), axis=1).tolist()

        # replace df NaN with empty string
        df = df.fillna('')

        properties = df.drop(['latitude', 'longitude'], axis=1).to_dict('records')

        feature_collection = FeatureCollection(features=features, properties=properties) # no crea el archivo correctamente

        with open(self.geojson_file, 'w') as f:
            json.dump(feature_collection, f, indent=4, ensure_ascii=False)


if __name__ == '__main__':
    """
    Main function.
    """
    csv_file = 'data/proyectos_geo.csv'
    geojson_file = 'data/proyectos.geojson'
    csv2geojson = Csv2Geojson(csv_file, geojson_file)
    csv2geojson.csv2geojson()
