import pandas as pd
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="around_dh")

def geoname(name):
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



proyectos = pd.read_csv('data/around_geo.csv')
print(f"Initial count: {proyectos.shape[0]}")

proyectos['latitude'], proyectos['longitude'] = zip(*proyectos['origen'].apply(geoname))

# remove rows where latitude is nan
proyectos = proyectos[pd.notnull(proyectos['latitude'])]

print(f"Final count: {proyectos.shape[0]}")

proyectos.to_csv('data/proyectos_geo.csv', index=False)
