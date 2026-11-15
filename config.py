###CONFIG FILE###

# ==========================================
# API CONFIGURATION
# ==========================================
wx_api_key = 'd5592d86a4e19a8e0e6ba345ca9cd54f'				#wait... might not need this

wx_url = "https://api.open-meteo.com/v1/forecast"
geo_url = "https://geocoding-api.open-meteo.com/v1/search"
snow_url = "https://wcc.sc.egov.usda.gov/awdbRestApi/services/v1/data"

# ==========================================
# COURT LOCATIONS
# ==========================================
pickle_locs = {'court': ['Sahalie', 'BP Elem', 'BP', 'GameFarm', 'Clarks Creek', 'Milton', 'Rainier Beach', 'Mercer', 'Shorewood'], 
               'lights': [1,0,0,1,1,1,1,0,0], 
               'lat': [47.299, 47.302, 47.302, 47.281, 47.185, 47.248, 47.524, 47.591, 47.753], 
               'long': [-122.352, -122.427, -122.440, -122.207, -122.32081, -122.3158, -122.274, -122.225, -122.350]
               }

indoor_courts = {
    "The Drop": [47.238955,-122.439934], #the drop
    "Rally": [47.282960,-122.235638], #rally
    "Fed Way Picklr": [47.355675,-122.311886]  #picklr

}

# ==========================================
# WEATHER SETTINGS
# ==========================================

day_or_not = {
    0: "night",
    1: "day"
}

#https://open-meteo.com/en/docs?daily=temperature_2m_max,temperature_2m_min,weather_code,sunrise,sunset,uv_index_max,apparent_temperature_max,apparent_temperature_min,precipitation_probability_max&hourly=&timezone=America%2FLos_Angeles&temperature_unit=fahrenheit&wind_speed_unit=kn&precipitation_unit=inch&latitude=47.2529,26.3358,31.7587,31,NaN&longitude=-122.4443,127.8014,-106.4869,36,NaN
wx_params = {
    'latitude' : [],
    'longitude' : [],
	"daily": ["temperature_2m_max", "temperature_2m_min", "weather_code", "sunrise", "sunset", "uv_index_max", "apparent_temperature_max", "apparent_temperature_min", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max"],
	"current": ["temperature_2m", "is_day", "weather_code"],    
	"timezone": "auto",
	"wind_speed_unit": "kn",
	"temperature_unit": "fahrenheit",
	"precipitation_unit": "inch",
    "forecast_days": 7,
    "wind_speed_unit": "kn"
}

pickle_params = {
	"latitude": [],
	"longitude": [],
	"hourly": ["wind_speed_10m", "precipitation_probability", "apparent_temperature", "temperature_2m", "precipitation", "weather_code", "is_day"],
	"timezone": "America/Los_Angeles",
    "past_days": 0,
	"forecast_days": 7,
	"wind_speed_unit": "kn",
    "temperature_unit": "fahrenheit"
}

# ==========================================
# PICKLEBALL WEATHER SCORING
# ==========================================

wind_bins = [0, 3, 5, 10, 100]
wind_scores = [20, 5, 3, 0]

temp_bins = [-30, 32, 45, 65, 80, 90, 100, 150]
temp_scores = [5, 10, 15, 20, 16, 8, 2]

precip_bins = [0, 3, 25, 50, 75, 100]
precip_scores = [60, 40, 30, 10, 5]