import pandas as pd
from pandas.errors import EmptyDataError

# Read the data
try:
    propuesta = pd.read_csv('data/propuesta_proyectos.csv')
except EmptyDataError:
    print('El archivo data/propuesta_proyectos.csv está vacío')
    exit()

def registrar_proyecto(**kwargs):

    # Add the new project to the DataFrame
    propuesta.loc[len(propuesta)] = kwargs.values()

    # Save the DataFrame to the CSV file
    propuesta.to_csv('data/propuesta_proyectos.csv', index=False)


if __name__ == '__main__':
    columns = ["nombre","url","origen","idioma","licencia","tipo_proyecto","equipo","tema"]
    nombre = input("Nombre del proyecto: ")
    url = input("URL del proyecto: ")
    origen = input("Origen del proyecto: ")
    idioma = input("Idioma del proyecto: ")
    licencia = input("Licencia del proyecto: ")
    tipo_proyecto = input("Tipo de proyecto: ")
    equipo = input("Equipo del proyecto: ")
    tema = input("Tema del proyecto: ")
    registrar_proyecto(**dict(zip(columns, [nombre, url, origen, idioma, licencia, tipo_proyecto, equipo, tema])))
    print("Proyecto registrado")
    
