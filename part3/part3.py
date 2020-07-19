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

def generate_df(filepath):
    """Takes a json file containing weather data and only the data required to make the graphs and summaries in dictionary format.
    
    Args:
        filepath: A string representing the path of the json file.
    Returns:
        A dictionary containing only the measurments required for this program.
    """


    data_frame = {"Time": [], "Temp": [], "Real_Feel_Temp": [], "Weather_Text": [], "Precipitation": [], "UV_Index": [], "Is_Daytime": []}

    with open(filepath) as json_file:
        json_data = json.load(json_file)

    for hour in json_data:
        
        time = get_time(hour["LocalObservationDateTime"])   
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
    """Takes a dictionary of weather data and creates a box plot graph that shows the temperature vs real feel temperature. 
    
    Args:
        dataframe: A dictionary of weather measurements.
    """

    box_plot_df = {
        "Hour": dataframe["Time"],
        "Temperature": dataframe["Temp"],
        "Real Feel Temperature": dataframe["Real_Feel_Temp"]
    }

    box_fig = px.box(box_plot_df, y=["Temperature", "Real Feel Temperature"], title=f'Recorded Temperatures Over the Past {len(box_plot_df["Hour"])} Hours') 

    box_fig.update_layout(
    yaxis_title="Temperature (Celcius)",
    xaxis_title="Recorded Temperatures"
    )

    box_fig.show()


def create_weather_text_chart(dataframe):
    """Takes a dictionary of weather data and creates a bar chart graph that shows the incidence of weather events. 
    
    Args:
        dataframe: A dictionary of weather measurements.
    """

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

def format_weather_event_times(dataframe, weather_measurement):
    """Takes a dictionary of weather data and a parameter that indicates the measurement required.
    
    Args:
        dataframe: A dictionary of weather measurements.
    Returns:
        A tuple containing a value correlating to the weather_measurement parameter and a list of hours in which the value occurred.
    """
    value_to_match = 0
    list_of_value_occurrences = []

    if weather_measurement == "min-temp":
        value_to_match = min(dataframe["Temp"])
        list_of_value_occurences = [i for i, x in enumerate(dataframe["Temp"]) if x == value_to_match]

    elif weather_measurement == "max-temp":
        value_to_match = max(dataframe["Temp"])
        list_of_value_occurences = [i for i, x in enumerate(dataframe["Temp"]) if x == value_to_match]

    elif weather_measurement == "u-v":
        value_to_match = max(dataframe["UV_Index"])
        list_of_value_occurences = [i for i, x in enumerate(dataframe["UV_Index"]) if x == value_to_match]

    else:
        return         
    
    times_values_occurred = [f'{dataframe["Time"][i]}' for i in list_of_value_occurences]

    formatted_times = f""

    for index, item in enumerate(times_values_occurred):
        if index != len(times_values_occurred) - 1:
            formatted_times += f"{item}, "
        else:
            formatted_times += f"and {item}"

    return (value_to_match, formatted_times)


def export_historical_weather_summary(dataframe):
    """Takes a dictionary of weather data, creates a summary and saves it to a text file.
    
    Args:
        dataframe: A dictionary of weather measurements.
    """
    min_temp_times = format_weather_event_times(dataframe, "min-temp")
    max_temp_times = format_weather_event_times(dataframe, "max-temp")
    max_uv_times = format_weather_event_times(dataframe, "u-v")

    hrs_of_rain = 0
    total_rain = 0

    for precip in dataframe["Precipitation"]:
        if precip != 0:
            total_rain += precip
            hrs_of_rain += 1

    num_daylight_hours = 0

    for daytime in dataframe["Is_Daytime"]:
        if daytime:
            num_daylight_hours += 1

    text = f'The minimum temperature was {format_temperature(min_temp_times[0])} at {min_temp_times[1]}.\nThe maximum temperature was {format_temperature(max_temp_times[0])} at {max_temp_times[1]}.\nThe total rain fall was {total_rain}mm over {hrs_of_rain} hours.\nThe number of daylight hours was {num_daylight_hours}.\nThe maximum UV index was: {max_uv_times[0]} at {max_uv_times[1]}.'

    print()
    print(text)
    print()

    with open("saved_weather_reports/historical_weather_report.txt", "w+") as report:
        report.write(text)
        pass

          
df = generate_df("data/historical_24hours_a.json")
create_temperature_box_plots(df)
create_weather_text_chart(df)
export_historical_weather_summary(df)
