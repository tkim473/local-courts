from court_calc import get_pickle       #get_pickle function returns dataframe with wx data
import folium                           #library to position each plot
import pandas as pd
from folium.plugins import TimestampedGeoJson

court_dfs = get_pickle()

m = folium.Map(
    location=[47.299, -122.352],
    zoom_start=10,
    tiles="https://basemaps.cartocdn.com/rastertiles/light_all/{z}/{x}/{y}.png?key=cb1_55u1_1_66701def5ef9bb62fd2d66f9",
    attr="© OpenStreetMap contributors © CARTO"
)

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
    df['time'] = pd.to_datetime(df["date"]).dt.strftime("%Y-%m-%dT%H:%M:%S")
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
                    f"Time: {row['date']}<br>"
                    f"Playability Score: {row['pickle_score']}<br>"
                    f"Temperature: {row['temperature_2m']}°F<br>"
                    f"Wind: {row['wind_speed_10m']} mph<br>"
                    f"Precip Probability: {row['precipitation_probability']}%<br>"
                    f"Lights: {row['lights']}"
                ),
                "icon": "circle",
                "iconstyle": {
                    "fillColor": color,
                    "fillOpacity": 0.9,
                    "stroke": True,
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
    date_options="h:mm A"
).add_to(m)

m.save("index.html")
