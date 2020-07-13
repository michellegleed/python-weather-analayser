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

def generate_df(forecast_file):

    data_frame = {
 
    }

    list_of_times = []
    list_of_temps = []
    list_of_weather_text = []
    list_of_precipitation = []
    list_of_uv_index = []
    list_of_is_daytime = []

    with open(forecast_file) as json_file:
        json_data = json.load(json_file)

    for hour in json_data:
        
        date_time = hour["LocalObservationDateTime"]
        temp = hour["Temperature"]["Metric"]["Value"]
        weather_text = hour["WeatherText"]
        precipitation = hour["PrecipitationSummary"]["Precipitation"]["Metric"]["Value"]
        uv_index = hour["UVIndex"]
        is_daytime = hour["IsDayTime"]

        time = get_time(date_time)     

        list_of_times.append(time)
        list_of_temps.append(temp)
        list_of_weather_text.append(weather_text)
        list_of_precipitation.append(precipitation)
        list_of_uv_index.append(uv_index)
        list_of_is_daytime.append(is_daytime)
        
    data_frame["Time"] = list_of_times
    data_frame["Temp"] = list_of_temps
    data_frame["Weather_Text"] = list_of_weather_text
    data_frame["Precipitation"] = list_of_precipitation
    data_frame["UV_Index"] = list_of_uv_index   
    data_frame["Is_Daytime"] = list_of_is_daytime

    # data_frame["Percip24"] = json_data[0]["PrecipitationSummary"]["Past24Hours"]


    

    return data_frame

df = generate_df("data/historical_24hours_b.json")

weather_text_counts = {}

list_of_weather_text = df["Weather_Text"]

for item in list_of_weather_text:
    if item in weather_text_counts.keys():
        weather_text_counts[item] = weather_text_counts[item] + 1
    else:
        weather_text_counts[item] = 1

print(weather_text_counts)

text_option_list = []
qty_list = []

for k, v in weather_text_counts.items():
    text_option_list.append(k)
    qty_list.append(v)

print(text_option_list)
print(qty_list)

bar_chart_df = {"Text_Options": text_option_list, "Qtys": qty_list}

weather_text_chart = px.bar(bar_chart_df, x="Text_Options", y="Qtys", labels={"Text_Options": "Weather Description", "Qtys": "Duration (Hours)"}, title=f"Incidence of Weather Events in the Past {len(df['Weather_Text'])} Hours")

weather_text_chart.show()

def export_historical_weather_summary(data):
    print(data) # {
        # 'Time': ['15:55', '14:55', '13:55', '12:55', '11:55', '10:55'], 
        # 'Temp': [18.9, 20, 21.1, 20, 21.1, 20],
        #  'Weather_Text': ['Light rain', 'Light rain', 'Sunny', 'Sunny', 'Sunny', 'Sunny'],
        #  'Precipitation': [True, True, False, False, False, False], 
        # 'UV_Index': [0, 2, 3, 3, 3, 2]
        # }

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

    text = f'Min temp was: {min} at {data["Time"][min_index]} \nMax temp was: {max} at {data["Time"][max_index]} \nTotal rain precipitation was {total_rain}mm over {hrs_of_rain} hours\nThe number of daylight hours was {num_daylight_hours} \nMax UV Index was: {max_uv} at {data["Time"][max_uv_index]}'

    print(text)

    with open("historical_weather_report.txt", "w+") as report:
        report.write(text)
          

export_historical_weather_summary(df)