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

    data_frame = {"Day": [], "Minimum Temp": [], "Maximum Temp": [], "Minimum Real Feel Temp": [], "Minimum Real Feel Shade Temp": []}

    with open(forecast_file) as json_file:
        json_data = json.load(json_file)
        daily_forecast_data = json_data["DailyForecasts"]

    for day in daily_forecast_data:

        date = convert_date(day["Date"])

        min_temp = convert_f_to_c(day["Temperature"]["Minimum"]["Value"])

        max_temp = convert_f_to_c(day["Temperature"]["Maximum"]["Value"])

        min_rf = convert_f_to_c(day["RealFeelTemperature"]["Minimum"]["Value"])

        min_rf_shade = convert_f_to_c(day["RealFeelTemperatureShade"]["Minimum"]["Value"])
    
        data_frame["Day"].append(date)
        data_frame["Minimum Temp"].append(min_temp)
        data_frame["Maximum Temp"].append(max_temp)
        data_frame["Minimum Real Feel Temp"].append(min_rf)
        data_frame["Minimum Real Feel Shade Temp"].append(min_rf_shade)

    # print(data_frame)

    return data_frame


df = generate_df("data/forecast_10days.json")

fig1 = px.line(df, x="Day", y=["Minimum Temp","Maximum Temp"], title="Daily Minimum and Maximum Temperature Predictions")


fig2 = px.line(df, x="Day", y=["Minimum Temp","Minimum Real Feel Temp","Minimum Real Feel Shade Temp"], title="Daily Temperature Predictions")

fig1.update_layout(
    yaxis_title="Temperature (Celcius)",
    legend_title="Key:"
)

fig2.update_layout(
    yaxis_title="Temperature (Celcius)",
    legend_title="Key:"
)

fig1.show()
fig2.show()
