import json
from datetime import datetime
import plotly.express as px

# A single time series graph that contains both the minimum and maximum temperatures for each day.

def convert_date(iso_string):
    """Converts and ISO formatted date into a human readable format.
    
    Args:
        iso_string: An ISO date string..
    Returns:
        A date formatted like: Weekday Date Month Year
    """

    d = datetime.strptime(iso_string, "%Y-%m-%dT%H:%M:%S%z")
    return d.strftime('%A %d %B %Y')

def convert_f_to_c(temp_in_farenheit):
    """Converts a temperature from farenheit to celcius

    Args:
        temp_in_farenheit: integer representing a temperature.
    Returns:
        An integer representing a temperature in degrees celcius.
    """

    celcius = (temp_in_farenheit - 32) * 5/9

    return round(celcius, 1)

def generate_df(forecast_file):

    data_frame = {
 
    }

    list_of_mins = []
    list_of_maxs = []
    list_of_days = []
    list_of_min_rf = []
    list_of_min_rf_shade = []

    with open(forecast_file) as json_file:
        json_data = json.load(json_file)
        daily_forecast_data = json_data["DailyForecasts"]

    for day in daily_forecast_data:

        iso_date = day["Date"]
        formatted_date = convert_date(iso_date)

        min_temp_farenheit = day["Temperature"]["Minimum"]["Value"]
        min_temp_celcius = convert_f_to_c(min_temp_farenheit)

        max_temp_farenheit = day["Temperature"]["Maximum"]["Value"]
        max_temp_celcius = convert_f_to_c(max_temp_farenheit)

        min_real_feel_farenheit = day["RealFeelTemperature"]["Minimum"]["Value"]
        min_rf_celcius = convert_f_to_c(min_real_feel_farenheit)

        min_rf_shade_farenheit = day["RealFeelTemperatureShade"]["Minimum"]["Value"]
        min_rfs_celcius = convert_f_to_c(min_rf_shade_farenheit)

        list_of_mins.append(min_temp_celcius)
        list_of_maxs.append(max_temp_celcius)
        list_of_days.append(formatted_date)
        list_of_min_rf.append(min_rf_celcius)
        list_of_min_rf_shade.append(min_rfs_celcius)
        
        # data_frame["max"] = data_frame["max"].append(max_temp_celcius)
        # data_frame["day"] = data_frame["day"].append(formatted_date)
    
    data_frame["Minimum Temp"] = list_of_mins
    data_frame["Maximum Temp"] = list_of_maxs
    data_frame["Day"] = list_of_days
    data_frame["Minimum Real Feel Temp"] = list_of_min_rf
    data_frame["Minimum Real Feel Shade Temp"] = list_of_min_rf_shade    

    print(data_frame)

    return data_frame


df = generate_df("data/forecast_5days_a.json")

# df = {
#     "min": [123, 132, 654, 345, 125, 498],
#     "max": [345, 67, 176, 245, 197, 391],
#     "day": ["M", "T", "W", "T", "F", "S"]
# }

fig1 = px.line(df, x="Day", y=["Minimum Temp","Maximum Temp"])
fig1.show()

fig2 = px.line(df, x="Day", y=["Minimum Temp","Minimum Real Feel Temp","Minimum Real Feel Shade Temp"])
fig2.show()
