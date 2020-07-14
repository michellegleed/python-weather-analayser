import json
from datetime import datetime
import plotly.express as px

def get_time(iso_string):
    """Extracts 24hr time from ISO date string.
    
    Args:
        iso_string: An ISO date string..
    Returns:
        time: hh:mm in 24-hr format
    """

    time = iso_string[11:16]

    return time

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees and celcius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and 'degrees celcius.'
    """

    return f"{temp}{DEGREE_SYBMOL}"

def generate_df(forecast_file):

    data_frame = {"Time": [], "Temp": [], "Real_Feel_Temp": [], "Weather_Text": [], "Precipitation": [], "UV_Index": [], "Is_Daytime": []}

    with open(forecast_file) as json_file:
        json_data = json.load(json_file)

    for hour in json_data:
        
        date_time = hour["LocalObservationDateTime"]
        time = get_time(date_time)   
        
        temp = hour["Temperature"]["Metric"]["Value"]
        weather_text = hour["WeatherText"]
        rf_temp = hour["RealFeelTemperature"]["Metric"]["Value"]
        precipitation = hour["PrecipitationSummary"]["Precipitation"]["Metric"]["Value"]
        uv_index = hour["UVIndex"]
        is_daytime = hour["IsDayTime"]

        data_frame["Time"].append(time)
        data_frame["Temp"].append(temp)
        data_frame["Real_Feel_Temp"].append(rf_temp)
        data_frame["Weather_Text"].append(weather_text)
        data_frame["Precipitation"].append(precipitation)
        data_frame["UV_Index"].append(uv_index)
        data_frame["Is_Daytime"].append(is_daytime)
    
    return data_frame

def create_temperature_box_plots(dataframe):
    
    box_plot_df = {
        "Hour": dataframe["Time"],
        "Temperature": dataframe["Temp"],
        "Real Feel Temperature": dataframe["Real_Feel_Temp"]
        
    }

    box_fig = px.box(box_plot_df, y=["Temperature", "Real Feel Temperature"]) 

    box_fig.update_layout(
    yaxis_title="Temperature (Celcius)",
    xaxis_title="Recorded Temperatures"
)

    box_fig.show()



def create_weather_text_chart(dataframe):

    weather_text_counts = {}

    list_of_weather_text = dataframe["Weather_Text"]

    for item in list_of_weather_text:
        if item in weather_text_counts.keys():
            weather_text_counts[item] = weather_text_counts[item] + 1
        else:
            weather_text_counts[item] = 1

    text_option_list = []
    qty_list = []

    for k, v in weather_text_counts.items():
        text_option_list.append(k)
        qty_list.append(v)

    bar_chart_df = {"Text_Options": text_option_list, "Qtys": qty_list}

    weather_text_chart = px.bar(bar_chart_df, x="Text_Options", y="Qtys", labels={"Text_Options": "Weather Description", "Qtys": "Duration (Hours)"}, title=f"Incidence of Weather Events in the Past {len(dataframe['Weather_Text'])} Hours")

    weather_text_chart.show()


def export_historical_weather_summary(data):

    min = 100
    min_index = 0

    max = 0
    max_index = 0

    for index, temp in enumerate(data["Temp"]):
        if temp < min:
            min = temp
            min_index = index
        if temp > max:
            max = temp
            max_index = index

    max_uv = 0
    max_uv_index = 0

    for index, uv in enumerate(data["UV_Index"]):
        if uv > max_uv:
            max_uv = uv
            max_uv_index = index

    hrs_of_rain = 0
    total_rain = 0

    for precip in data["Precipitation"]:
        if precip != 0:
            total_rain += precip
            hrs_of_rain += 1

    num_daylight_hours = 0

    for daytime in data["Is_Daytime"]:
        if daytime:
            num_daylight_hours += 1

    text = f'Min temp was: {format_temperature(min)} at {data["Time"][min_index]}.\nMax temp was: {format_temperature(max)} at {data["Time"][max_index]}.\nTotal rain fall was {total_rain}mm over {hrs_of_rain} hours.\nThe number of daylight hours was {num_daylight_hours}.\nMax UV Index was: {max_uv} at {data["Time"][max_uv_index]}.'

    print()
    print(text)
    print()

    with open("saved_weather_reports/historical_weather_report.txt", "w+") as report:
        report.write(text)

          
df = generate_df("data/historical_24hours_a.json")
create_temperature_box_plots(df)
create_weather_text_chart(df)
export_historical_weather_summary(df)