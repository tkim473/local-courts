from config import *
import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
import numpy as np
import matplotlib.pyplot as plt
from functools import reduce
from datetime import date



def get_pickle():
    pickle_params['latitude'] = pickle_locs['lat']
    pickle_params['longitude'] = pickle_locs['long']
    # Setup the Open-Meteo API client with cache and retry on error
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    openmeteo = openmeteo_requests.Client(session = retry_session)


    responses = openmeteo.weather_api(wx_url, params = pickle_params)         #url and params in config file
    # Process first location. Add a for-loop for multiple locations or weather models
    i = 0           #index to iterate through pickle_loc names
    pickledf_list = []

    for response in responses:
        
        # Process hourly data. The order of variables needs to be the same as requested.
        hourly = response.Hourly()
        hourly_wind_speed_10m = hourly.Variables(0).ValuesAsNumpy()
        hourly_precipitation_probability = hourly.Variables(1).ValuesAsNumpy()
        hourly_apparent_temperature = hourly.Variables(2).ValuesAsNumpy()
        hourly_temperature_2m = hourly.Variables(3).ValuesAsNumpy()
        hourly_precipitation = hourly.Variables(4).ValuesAsNumpy()
        hourly_weather_code = hourly.Variables(5).ValuesAsNumpy()
        hourly_is_day = hourly.Variables(6).ValuesAsNumpy()

        hourly_data = {"date": pd.date_range(
	        start = pd.to_datetime(hourly.Time() + response.UtcOffsetSeconds(), unit = "s", utc = True),
	        end =  pd.to_datetime(hourly.TimeEnd() + response.UtcOffsetSeconds(), unit = "s", utc = True),
	        freq = pd.Timedelta(seconds = hourly.Interval()),
	        inclusive = "left"
        )}

        hourly_data["wind_speed_10m"] = hourly_wind_speed_10m
        hourly_data["precipitation_probability"] = hourly_precipitation_probability
        hourly_data["apparent_temperature"] = hourly_apparent_temperature
        hourly_data["temperature_2m"] = hourly_temperature_2m
        hourly_data["precipitation"] = hourly_precipitation
        hourly_data["weather_code"] = hourly_weather_code
        hourly_data["is_day"] = hourly_is_day
        hourly_data['court'] = pickle_locs['court'][i]
        hourly_data['lights'] = pickle_locs['lights'][i]
        
        
        #scoring for each variable: wind, precip, temp, day
        hourly_data['wind_score'] = pd.cut(hourly_data['wind_speed_10m'], bins = wind_bins, labels = wind_scores, include_lowest=True).astype(float)
        hourly_data['temp_score'] = pd.cut(hourly_data['temperature_2m'], bins = temp_bins, labels = temp_scores, include_lowest=True).astype(float)
        hourly_data['precip_score'] = pd.cut(hourly_data['precipitation_probability'], bins = precip_bins, labels = precip_scores, include_lowest=True).astype(float)


        hourly_dataframe = pd.DataFrame(data = hourly_data)
        hourly_dataframe.set_index('date', inplace = True)
        hourly_dataframe.loc[hourly_dataframe.between_time("22:00", "06:00").index, 'lights'] = 0
        hourly_dataframe = hourly_dataframe.reset_index()       #resetting it to numerical cause I'm dumb and having issues
        
        hourly_dataframe['light_score'] = hourly_dataframe['is_day'] + hourly_dataframe['lights']
        hourly_dataframe['light_multiplier'] = np.where(hourly_dataframe['light_score'] > 0, 1, 0)
        hourly_dataframe['pickle_score'] = (hourly_dataframe['wind_score'] + hourly_dataframe['temp_score'] + hourly_dataframe['precip_score'])*hourly_dataframe['light_multiplier']

        i += 1 #for court names
        pickledf_list.append(hourly_dataframe)


   
    return pickledf_list





def plot_pickle():
    df_list = get_pickle()

    fig, axs = plt.subplots(4,2, figsize = (11,12), sharey = True)
    axs = axs.flatten()
    for index, df in enumerate(df_list):

        court = df['court'].iloc[0]     #get court name from dataframe

        #pickle_score already has a light multiplier making it 0 when its dark. Just turn the rest of the scores 0 if the overall score is 0. 
        #It's a little backwards. 
        
        df.loc[df['pickle_score']==0, ['wind_score', 'temp_score', 'precip_score']] = 0     #if pickle_score is 0 (its already )
        
        df['hour'] = df['date'].dt.strftime('%H:00')
        df['wind_str'] = df['wind_speed_10m'].map(lambda x:f"{x:.1f}kt")
        df['temp_str'] = df['temperature_2m'].map(lambda x:f"{x:.0f}F")
        df['prec_str'] = df['precipitation_probability'].map(lambda x:f"{x:.1f}%")

        #convert some of the labels to ' ' blank values where pickle_score is 0. 
        df.loc[df['pickle_score']==0, ['wind_str', 'temp_str', 'prec_str']] = '' 
        ax = axs[index]
        #make the background asthetically pleasing
        ax.axhspan(80, 100, color = 'green', alpha=.2)
        ax.axhspan(50, 80, color = 'yellow', alpha=.1)
        ax.axhspan(00, 50, color = 'red', alpha=.1)

        #referencing ax (which is defined as axs[index]) in the .plot.bar call is what makes it utilize the previously created subplot. Without this, it will create individual plts. 
        df[['hour','precip_score', 'temp_score', 'wind_score']].plot.bar(x='hour',stacked = True, align = 'edge', width = .95, ax = ax)
        ax.set_title(court)
        
        #column names to pull from df dataframe are iterated through
        for c, col in zip(ax.containers, [ 'prec_str', 'temp_str', 'wind_str']):
            rot = 45 if col == 'wind_str' else 90        #formatting so that wind_str is horizontal
            lab_type = 'edge' if col == 'wind_str' else 'center'
            ax.bar_label(c, labels = df[col], label_type=lab_type, rotation = rot)



    plt.tight_layout()      #automatically adjust layout to prevent overlapping titles
    today = date.today()
    fig.suptitle(f'Local Tennis Court Playability {today}')
    return fig, axs     #return tuple

plot_pickle()
