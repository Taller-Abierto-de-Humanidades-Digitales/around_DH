import pandas as pd
from geopy.geocoders import Nominatim
import os
from csv2geojson import Csv2Geojson
from datetime import datetime

geolocator = Nominatim(user_agent="around_dh")


class Geoconvert:

    def __init__(self, proyectos, proyectos_geo):
        self.proyectos = os.path.join(os.path.dirname(__file__), proyectos)
        self.proyectos_geo = os.path.join(
            os.path.dirname(__file__), proyectos_geo)

    def geoname(self, name):
        location = geolocator.geocode(name)
        print(name)
        try:
            print(location.latitude, location.longitude)
            return location.latitude, location.longitude
        except AttributeError:
            name_attempt = name.split(',')[0]
            location = geolocator.geocode(name_attempt)
            print(f"Intentando nuevamente con {name_attempt}")
            try:
                print(location.latitude, location.longitude)
                return location.latitude, location.longitude
            except AttributeError:
                name_attempt2 = name_attempt.split('.')[0]
                location = geolocator.geocode(name_attempt2)
                print(f"Intentando por segunda vez con {name_attempt2}")
                try:
                    print(location.latitude, location.longitude)
                    return location.latitude, location.longitude
                except AttributeError:
                    print(f"No se pudo geolocalizar {name}")
                    return None, None

    def geolocalize(self):
        proyectos = pd.read_csv(self.proyectos)

        print(f"Proyectos a actualizar: {proyectos.shape[0]}")

        proyectos['latitude'], proyectos['longitude'] = zip(
            *proyectos['origen'].apply(self.geoname))

        # remove rows where latitude is nan
        proyectos = proyectos[pd.notnull(proyectos['latitude'])]

        print(f"Proyectos a actualizar (lista depurada): {proyectos.shape[0]}")

        self.toLog(
            f"Proyectos a actualizar ({proyectos.shape[0]}): {proyectos['nombre'].tolist()}")

        return proyectos

    def merge_geolocalize(self):
        proyectos = self.geolocalize()
        mergewith = pd.read_csv(self.proyectos_geo)
        print(f"Proyectos originales: {mergewith.shape[0]}")

        conjunto_proyectos = pd.concat(
            [mergewith, proyectos], ignore_index=True)
        print(f"Proyectos actualizados: {conjunto_proyectos.shape[0]}")

        assert conjunto_proyectos.shape[0] == mergewith.shape[0] + \
            proyectos.shape[0]

        return conjunto_proyectos

    def clean_propuesta_proyectos(self):
        '''
        remove all rows in propuesta_proyectos.csv
        '''
        propuesta_proyectos = pd.read_csv(self.proyectos)
        propuesta_proyectos.drop(propuesta_proyectos.index, inplace=True)
        propuesta_proyectos.to_csv(self.proyectos, index=False)

    def toLog(self, message):
        os.makedirs("logs", exist_ok=True)
        with open('logs/log.txt', 'a') as f:
            f.write(datetime.now().strftime(
                "%d/%m/%Y %H:%M:%S") + ": " + message + '\n')

    def save_geolocalize(self):
        guardar_proyecto = self.merge_geolocalize()
        guardar_proyecto.sort_values(by=['nombre'], inplace=True)
        guardar_proyecto.drop_duplicates(
            subset=['nombre'], inplace=True, keep='first')
        guardar_proyecto.to_csv(self.proyectos_geo, index=False)
        self.clean_propuesta_proyectos()
        self.toLog(f"Proyectos actualizados: {guardar_proyecto.shape[0]}")


if __name__ == "__main__":
    geoconvert = Geoconvert(
        "data/propuesta_proyectos.csv", "data/proyectos_geo.csv")
    geoconvert.save_geolocalize()
    #csv2geojson = Csv2Geojson("data/proyectos_geo.csv", "data/proyectos.geojson")
    # csv2geojson.csv2geojson()
