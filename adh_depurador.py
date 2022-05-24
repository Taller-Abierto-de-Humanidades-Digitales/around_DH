"""
This script functionality is to be used to depurate the data from the AroundDH csv file.
The source of the data is the AroundDH spreadsheet: https://docs.google.com/spreadsheets/d/1_PNv9Jlw_QlUh6SeYJrGYFucoRzlZAfLf7OouWu-qe4/edit?usp=sharing
"""

from cmath import nan
import pandas as pd
import requests
from requests.exceptions import ConnectionError, MissingSchema

around = pd.read_csv("data/AroundDH.csv")

# remove rows if Project is nan
around = around[pd.notnull(around['Link'])]
around = around[pd.notnull(around['Location(s): Production'])]

around['origen'] = around['Location(s): Production'].apply(
    lambda x: x.split(';')[0] if pd.notnull(x) else nan)

links = around['Link'].to_list()

# remove non string values from links
links = [link for link in links if isinstance(link, str)]

useful_links = []
bad_links = []

for link in links:
    try:
        r = requests.get(link)
        print(link, r.status_code)
        if r.status_code == 200 or r.status_code == 406:
            useful_links.append(link)
        else:
            bad_links.append(f"{link} || {r.status_code}")
    except ConnectionError as e:
        print("Error for URL: {}".format(link))
        bad_links.append(f"{link} || {e.__class__.__name__}")
        pass
    except MissingSchema as e:
        link = link.split(' / ')[0]
        try:
            '''
            trying to resolve errors in links withouth http://
            '''
            r = requests.get(f"http://{link}")
            print(f"{link} || {r.status_code}")
            if r.status_code == 200:
                useful_links.append(f"http://{link}")
            else:
                bad_links.append(f"{link} || {r.status_code}")
        except ConnectionError as e:
            print("Error for URL: {}".format(link))
            bad_links.append(f"{link} || {e.__class__.__name__}")
            pass
        except MissingSchema as e:
            print("Error for URL: {}".format(link))
            bad_links.append(f"{link} || {e.__class__.__name__}")
            pass


# select only useful links from around
around = around[around['Link'].isin(useful_links)]


around = around[['Project', 'Team', 'Link',
                 'origen', 'Location(s): Theme', 'Notes']]

# rename columns
around.columns = ['nombre', 'equipo', 'url', 'origen', 'tema', 'tipo_proyecto']

proyectos = pd.read_csv("data/proyectos.csv")

# merge around and proyectos
around.merge(proyectos, on=['nombre', 'url', 'origen', 'tipo_proyecto'])

around.to_csv("data/around_geo.csv", index=False)

# save bad links as txt
with open("data/broken_links.txt", "w") as f:
    for link in bad_links:
        f.write(link + "\n")
