#Webmap that displays the volcanoes in the state of US , and also displays the population density among diff continents
# folium - webmap methods
import folium
#to read data from the given txt file
import pandas

data = pandas.read_csv("Volcanoes.txt")

#creating list of values in 'LAT' col of data
lat = list(data['LAT'])
lon = list(data['LON'])
elev = list(data['ELEV'])
name = list(data['NAME'])

#coloring the markers based on the elevation of the volcano mountains
def color_producer(elevation):
    if elevation<1000:
        return 'green'
    elif 1000<=elevation< 3000:
        return 'orange'
    else:
        return 'red'

#creating a plain webmap
map = folium.Map(location=[38.58,-99.99],zoom_start = 4)

#feature grps added to the layer ctrl , can be controled from the top rgt hand corner icon
fgv = folium.FeatureGroup(name = 'Volcanoes')
fgp = folium.FeatureGroup(name = 'Population')

#html text to be inserted in the popup
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
#zip enables to iterate simultaneously through more than one object
for lt,ln,el,nm in zip(lat,lon,elev,name):
    #the popup frame
    iframe = folium.IFrame(html = html % (nm,nm,el), width = 200, height = 100)
    #adding the volacano markers
    fgv.add_child(folium.CircleMarker(location = [lt,ln],radius=6,popup = folium.Popup(iframe),fill_color=color_producer(el),color='grey',fill_opacity=0.7))

#adding boundaries to the map for some of the continents, multipolygonal layer with colors for the pop density
fgp.add_child(folium.GeoJson(data = open('world.json','r',encoding = 'utf-8-sig').read(),
style_function = lambda x: {'fillColor':'green' if x['properties']['POP2005']<10000000
else 'orange' if 10000000 <=x['properties']['POP2005']<20000000 else 'red'}))

#adding both feature grps to the parent map
map.add_child(fgv)
map.add_child(fgp)

#adding layer control for the above feature grps, to be applied after adding all the child layers
map.add_child(folium.LayerControl())

#saving the file in the current directory
map.save('Map_USvolcanoes&population.html')
