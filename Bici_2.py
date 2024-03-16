#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import requests as req
import ast # Desglosar una columna
import numpy as np
from shapely.geometry import Point  #Hacer lineas en el mapa
import geopandas as gpd # Importar el mp
import argparse
from fuzzywuzzy import fuzz #Compar dos string y devuelve un valor de similitud


# In[2]:


est_bicimad= pd.read_csv("C:/Users/hp/OneDrive/Imágenes/Proyectos/bicimad_stations.csv", sep="\t")  #separar con la t (tabulador)

est_bicimad.head()


# In[3]:


len(est_bicimad)


# In[4]:


#desglosar coordinates
est_bicimad["geometry.coordinates"] = est_bicimad["geometry.coordinates"].apply(ast.literal_eval) #separar la columna en dos
est_bicimad['Latitudes'] = est_bicimad['geometry.coordinates'].apply(lambda x: x[1]) #columna 1 
est_bicimad["Longitudes"] = est_bicimad["geometry.coordinates"].apply(lambda x: x[0])


# In[5]:


est_bicimad.head() #Comprobar esta bien


# In[46]:


#Quitar columnas y renombrar

est_bicimad.pop("geometry.coordinates")
est_bicimad.pop("geometry.type")
est_bicimad.pop("Unnamed: 0")
est_bicimad.pop("id")
est_bicimad.pop("number")

df_bicimad= est_bicimad.rename(columns={"name":"localizacion", "light": "ocupación", "no_available":"disponibilidad", "Latitudes":"latitud","Longitudes":"longitud"})
df_bicimad['localizacion'] = df_bicimad['localizacion'].apply(lambda x: x.split('-')[-1])


df_bicimad


# In[7]:


url= "https://datos.madrid.es/egob/catalogo/203166-0-universidades-educacion.json"

#res: responder a la url anterior.

res= req.get(url) #Traer la url anterior.

universidades= res.json().keys() #Nombres clave de los dos grandes diccionarios

universidades= res.json()["@graph"] #Selecciono el diccionario grph


# In[8]:


datos_universidades= pd.json_normalize(universidades) #generar tabla con todo lo que tiene el graph

datos_universidades

datos_universidades.pop("@id")
datos_universidades.pop("@type")
datos_universidades.pop("id")
datos_universidades.pop("address.district.@id")
datos_universidades.pop("relation")
datos_universidades.pop("address.area.@id")
datos_universidades.pop("address.locality")
datos_universidades.pop("organization.services")
datos_universidades.pop("organization.schedule")
datos_universidades.pop("address.postal-code")
datos_universidades.pop("organization.accesibility")
datos_universidades.pop("organization.organization-name")

df_universidades = datos_universidades.rename(columns={"address.street-address": "dirección", "location.latitude":"latitud", "title":"nombre","location.longitude": "longitud" })

df_universidades


# In[9]:


def to_mercator(lat, long):
    # transform latitude/longitude data in degrees to pseudo-mercator coordinates in metres
    c = gpd.GeoSeries([Point(lat, long)], crs=4326)
    c = c.to_crs(3857)
    return c
    
def distance_meters(lat_start, long_start, lat_finish, long_finish):
    # return the distance in metres between to latitude/longitude pair points in degrees 
    # (e.g.: Start Point -> 40.4400607 / -3.6425358 End Point -> 40.4234825 / -3.6292625)
    start = to_mercator(lat_start, long_start)
    finish = to_mercator(lat_finish, long_finish)
    return start.distance(finish)

def cercania(df1,df2):
    paradas_cercanas=[]
    for columna1, fila1 in df1.iterrows():  #recorrer las siguientes filas 
        min_distancia=np.inf #distancia en positivo
        punto_cercano= None
        for columna2, fila2 in df2.iterrows():
            distancia = distance_meters(fila1["latitud"], fila1["longitud"], fila2["latitud"], fila2["longitud"])      
            if distancia.min() < min_distancia: # Si la distancia es menor que la mínima distancia, es decir, un punto más cercano a la distancia real se desecha el anterior que sería la distancia por la mínima distancia
                min_distancia = distancia.min()
                punto_cercano = columna2
        paradas_cercanas.append(punto_cercano)
    return paradas_cercanas


# In[25]:


#Convertir la latitud y la longitud en un float

df_bicimad["latitud"]=df_bicimad["latitud"].astype(float)
df_bicimad["longitud"]=df_bicimad["longitud"].astype(float)
df_universidades["latitud"]=df_universidades["latitud"].astype(float)
df_universidades["longitud"]=df_universidades["longitud"].astype(float)


# In[26]:


origen= input("Seleccionar una universidad")
destino= input("seleccionar destino")


# In[27]:


df_bicimad["fuzzy"] = df_bicimad["localizacion"].apply(lambda x: fuzz.partial_ratio(x, origen))


df_bicimad_max = df_bicimad.nlargest(1, "fuzzy")

df_bicimad_max


# In[29]:


df_universidades["fuzzy"] = df_universidades["nombre"].apply(lambda x: fuzz.partial_ratio(x, destino))


df_universidades_max = df_bicimad.nlargest(1, "fuzzy")

df_universidades_max


# In[30]:


punto_cercano = cercania(df_universidades, df_bicimad)

df_universidades["parada_cercana"] = punto_cercano

df_universidadxbicimad = df_universidades.merge(df_bicimad, left_on="parada_cercana", right_index=True, suffixes=('_df1', '_df2'))

# Calcular la distancia entre cada universidad y su estación de BiciMAD más cercana
df_universidadxbicimad["distancia_metros"] = df_universidadxbicimad.apply(
    lambda row: distance_meters(row["latitud_df1"], row["longitud_df1"], row["latitud_df2"], row["longitud_df2"]),
    axis=1
)


# In[34]:


df_universidadxbicimad.head()


# In[43]:


columns= ["latitud_df1", "longitud_df1", "parada_cercana", "activate", "disponibilidad", "free_bases", "latitud_df2","longitud_df2", "fuzzy_df1", "fuzzy_df2","ocupación" ]

df_universidadxbicimad.drop(columns=columns)


# In[44]:


df_universidadxbicimad.to_csv('datos.csv', index=True)


# In[45]:


import argparse
import pandas as pd

parser = argparse.ArgumentParser(description='Bici Mad')

# definir argumentos de entrada, que luego voy a escribir en la terminal
parser.add_argument('-o', '--origin', type=str, help='Origen del usuario')
parser.add_argument('-d', '--destination', type=str, help='Destino del usuario')

# inicio el parser
parse_args = parser.parse_args()

origin = parse_args.origin
destino = parse_args.destination

print(origin, '---------', destino)

df = pd.read_csv('datos.csv')

df_filtrado = df[(df['nombre'] == origin) & (df['parada_cercana'] == destino)]

print(df)

print()

print(f'Hola, estas en {origin}, tu estacion mas cercana es {df_filtrado.iloc[0]}')


# In[ ]:




