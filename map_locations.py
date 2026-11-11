from court_calc import get_pickle       #get_pickle function returns dataframe with wx data
import folium                           #library to position each plot
import pandas as pd
from folium.plugins import TimestampedGeoJson

court_dfs = get_pickle()

m = folium.Map(
    location=[47.40, -122.29],
    zoom_start=10,
    tiles="https://basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png?key=cb1_55u1_1_66701def5ef9bb62fd2d66f9",
    attr="© OpenStreetMap contributors © CARTO"
)

#title
map_title = "Pickleball Court Weather"
title_html = f'<h1 style="position:absolute;z-index:100000; bottom: 24px; text-decoration: underline;" >{map_title}</h1>'
m.get_root().html.add_child(folium.Element(title_html))


kw = {"prefix": "fa", "color": "green", "icon": "warehouse"}
icon = folium.Icon(**kw)
#add static courts
indoor_courts = {
    "The Drop": [47.238955,-122.439934], #the drop
    "Rally": [47.282960,-122.235638], #rally
    "Fed Way Picklr": [47.355675,-122.311886]  #picklr

}


for court, loc in indoor_courts.items():
    folium.Marker(location=loc, icon=icon, popup = court).add_to(m)

#time now. will be used to generate colored dots for court scores
current_time_utc=pd.Timestamp.now(tz='UTC')

#create bins for color scale
bins = [-1, 50, 80, 100]  # -1 catches exactly 0 if needed
labels = ['red', 'yellow', 'green']

features = []

#add courts
#iterate through the dfs in court_dfs
for df in court_dfs:
    #add column for color status
    df['color_status'] = pd.cut(df['pickle_score'], bins=bins, labels=labels)
    df['time'] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%dT%H:%M")
    df['date_str'] = df['date'].dt.strftime("%a, %Y-%m-%d")
    df['time_str'] = df['date'].dt.strftime("%H:%M")
    df['temp'] = df['temperature_2m'].astype('float64').round(2)
    df['wind'] = df['wind_speed_10m'].astype('float64').round(2)

    for _, row in df.iterrows():

        color = row['color_status']


        features.append({
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [
                    row["long"],
                    row["lat"]
                ]
            },
            "properties": {
                "times": [row["time"]],
                "popup": (
                    f"<b>{row['court']}</b><br>"
                    f"Date: {row['date_str']}<br>"
                    f"Time: {row['time_str']}<br>"
                    f"Playability Score: {row['pickle_score']}<br>"
                    f"Temp: {row['temp']}°F<br>"
                    f"Wind: {row['wind']} mph<br>"
                    f"Precip Prob: {row['precipitation_probability']}%<br>"
                    f"Lights: {row['lights']}<br>"
                    
                ),
                "icon": "circle",
                "iconstyle": {
                    "fillColor": color,
                    "fillOpacity": 0.7,
                    "stroke": True,
                    "color": "black",
                    "weight": 1,
                    "radius": 9
                }
            }
        })




# Add time slider
TimestampedGeoJson(
    {
        "type": "FeatureCollection",
        "features": features
    },
    period="PT1H",
    duration="PT1H",
    auto_play=False,
    loop=False,
    add_last_point=True,
    time_slider_drag_update=True,
    date_options="dddd, MM/DD/YYYY h:mm A"
).add_to(m)

m.save("index.html")
