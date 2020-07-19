# -*- coding: utf-8 -*-
"""
Created on Fri May  1 12:00:12 2020

@author: abc
"""

import folium
import pandas as pd

def color_producer(el):
    if el<1000:
        return "green"
    elif 1000<=el<3000:
        return "orange"
    else:
        return "red"

df=pd.read_csv('volcanoes.txt')
names=list(df['NAME'])
lat=list(df['LAT'])
long=list(df['LON'])
elev = list(df["ELEV"])


html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""

map=folium.Map(location=[lat[0],long[0]],zoom_start=5,tiles = "Stamen Terrain")

fgv=folium.FeatureGroup(name='Volcanoes')

for lt,ln,name,el in zip(lat,long,names,elev):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    child=folium.Marker(location=[lt,ln],popup=folium.Popup(iframe),
                        icon=folium.Icon(color=color_producer(el)))
    fgv.add_child(child)

fgp=folium.FeatureGroup(name='Population')
child=folium.GeoJson(data=open('world.json','r',encoding='utf-8-sig').read(),
    style_function=lambda x:{'fillColor':'green' if x['properties']['POP2005']<1000000
                             else 'orange' if 1000000<=x['properties']['POP2005']<2000000
                             else 'red'})
fgp.add_child(child)
map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())

map.save('Map1.html')
