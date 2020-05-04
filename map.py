import csv
import json
import random
import time

import folium
import jinja2
import yaml

import pprint

env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))
tooltip_template = env.get_template('tooltip.html')
popup_template = env.get_template('popup.html')

with open('config.yaml', 'r') as ymlfile:
    cfg = yaml.full_load(ymlfile)

api_key = cfg.get('api_key')


def main():
    # Create map object
    m = folium.Map(location=[37.7627365, -122.4391288],
                   tiles='https://tile.thunderforest.com/spinal-map/{z}/{x}/{y}.png?apikey=' + api_key,
                   attr='Spinal Map',
                   zoom_start=11)

    cat_icons = list(json.load(open('static/cat_icons.json')).values())
    len_cat_icons = len(cat_icons)
    cat_index = 0

    print(f"number of cat markers: {len_cat_icons}")
    print(f"number of music studios in csv: {len(open('data/music_programs.csv').readlines()) - 1}")

    icons_added = 0
    with open('data/music_programs.csv') as fin:
        reader = csv.DictReader(fin)
        for row in reader:
            lat = float(row['lat'])
            lon = float(row['lon'])

            tooltip = tooltip_template.render(data=row)
            popup = popup_template.render(data=row)

            if cat_index >= len_cat_icons:
                cat_index = 0
            icon = cat_icons[cat_index]
            cat_index += 1

            folium.Marker([lat, lon],
                          popup=popup,
                          icon=folium.features.CustomIcon(
                icon['url'], icon_size=icon['icon_size']),
                tooltip=tooltip).add_to(m)
                
            icons_added += 1

    print(f"number of map icons added: {icons_added}")
    m.save('dist/index.html')


if __name__ == "__main__":
    main()
