import folium
import pandas


data = pandas.read_csv('Volcanoes.txt')

latitude = list(data['LAT'])
longitude = list(data['LON'])
name = list(data['NAME'])
elevation = list(data['ELEV'])

map = folium.Map(location=[20, 78], zoom_start=5, tiles='Stamen Terrain')


def color_ranger(elevation):
    if elevation <= 1000:
        return 'green'
    elif 1000 < elevation <= 3000:
        return 'orange'
    else:
        return 'red'


feature_group_volcano = folium.FeatureGroup(name='Volcanoes')

for lat, lon, vol_name, elev in zip(latitude, longitude, name, elevation):
    feature_group_volcano.add_child(
        folium.Marker(
            location=[lat, lon],
            popup=f'{vol_name} : {elev} m',
            icon=folium.Icon(
                color=color_ranger(elev)
            )
        )
    )

feature_group_population = folium.FeatureGroup(name='Population')

feature_group_population.add_child(
    folium.GeoJson(
        data=open(
            'world.json', 'r',
            encoding='utf-8-sig'
        ).read(),
        style_function=lambda x: {
            'fillColor': 'lemon'
            if x['properties']['POP2005'] < 10000000 else 'orange'
            if 10000000 <= x['properties']['POP2005'] < 20000000 else 'red'
        }
    )
)


map.add_child(feature_group_volcano)
map.add_child(feature_group_population)

map.add_child(folium.LayerControl())

map.save('index.html')

