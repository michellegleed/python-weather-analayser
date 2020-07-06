import json
from datetime import datetime

DEGREE_SYBMOL = u"\N{DEGREE SIGN}C"

def format_temperature(temp):
    """Takes a temperature and returns it in string format with the degrees and celcius symbols.
    
    Args:
        temp: A string representing a temperature.
    Returns:
        A string contain the temperature and 'degrees celcius.'
    """
    return f"{temp}{DEGREE_SYBMOL}"

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
    # print(celcius)
    # print(round(celcius))

    return round(celcius, 1)


def calculate_mean(total, num_items):
    """Calculates the mean.
    
    Args:
        total: integer representing the sum of the numbers.
        num_items: integer representing the number of items counted.
    Returns:
        An integer representing the mean of the numbers.
    """
    return round(total / num_items, 1)

def generate_overview(daily_forecast_data):
    min_temps = {}  
    max_temps = {}

    sum_of_mins = 0
    sum_of_maxs = 0

    for day in daily_forecast_data:
        iso_date = day["Date"]
        min = day["Temperature"]["Minimum"]["Value"]
        max = day["Temperature"]["Maximum"]["Value"]

        sum_of_mins += min
        sum_of_maxs += max

        min_temps[iso_date] = min
        max_temps[iso_date] = max
    
    ave_min = calculate_mean(sum_of_mins, len(daily_forecast_data))

    ave_max = calculate_mean(sum_of_maxs, len(daily_forecast_data))

    min_temp = 100
    min_date = ""

    max_temp = 0
    max_date = ""

    for date, temp in min_temps.items():
        if temp < min_temp:
            min_temp = temp
            min_date = date
        else:
            continue

    for date, temp in max_temps.items():
        if temp > max_temp:
            max_temp = temp
            max_date = date
        else:
            continue
    
    min_celcius = format_temperature(convert_f_to_c(min_temp))
    max_celcius = convert_f_to_c(max_temp)

    ave_min_celcius = convert_f_to_c(ave_min)

    ave_max_celcius = convert_f_to_c(ave_max)

    return f"{len(daily_forecast_data)} Day Overview\n {'':>3}The lowest temperature will be {min_celcius}, and will occur on {convert_date(min_date)}.\n{'':>3} The highest temperature will be {format_temperature(max_celcius)}, and will occur on {convert_date(max_date)}.\n{'':>3} The average low this week is {format_temperature(ave_min_celcius)}.\n{'':>3} The average high this week is {format_temperature(ave_max_celcius)}.\n\n"
    
    

    
    
    # print(f"")
    # print()

    

    # print(f"{'':>10} The average low this week is {format_temperature(ave_min_celcius)}")
    # print()

    # print(f"{'':>10} The average high this week is {format_temperature(ave_max_celcius)}")
    # print()
    # print()



    
def generate_summary(daily_forecast_data):

    output = ""

    for day in daily_forecast_data:
        iso_date = day["Date"]
        formatted_date = convert_date(iso_date)
        # print(f"-------- {formatted_date} --------")
        # print()

        min_temp_farenheit = day["Temperature"]["Minimum"]["Value"]
        min_temp_celcius = convert_f_to_c(min_temp_farenheit)
        
        # print("Minimum Temperature:", format_temperature(min_temp_celcius))
        # print()

        max_temp_farenheit = day["Temperature"]["Maximum"]["Value"]
        max_temp_celcius = convert_f_to_c(max_temp_farenheit)
        
        # print("Minimum Temperature:", format_temperature(max_temp_celcius))
        # print()

        day_desc = day["Day"]["LongPhrase"]
        
        # print("Daytime:", day_desc)
        # print()

        day_rain_probability = day["Day"]["RainProbability"]
        
        # print(f"{'':>5}Chance of rain: {day_rain_probability}%")
        # print()

        night_desc = day["Night"]["LongPhrase"]
        
        # print("Nighttime:", night_desc)
        # print()

        night_rain_probability = day["Night"]["RainProbability"]
        
        # print(f"{'':>5}Chance of rain: {night_rain_probability}%")
        # print()
        # print()

        formatted_day = f"-------- {formatted_date} --------\nMinimum Temperature: {format_temperature(min_temp_celcius)}\nMaximum Temperature: {format_temperature(max_temp_celcius)}\nDaytime: {day_desc}\n{'':>3} Chance of rain:  {day_rain_probability}%\nNighttime: {night_desc}\n{'':>3} Chance of rain:  {night_rain_probability}%\n\n"    
        
        output += formatted_day
    
    return output


def process_weather(forecast_file):
    """Converts raw weather data into meaningful text.

    Args:
        forecast_file: A string representing the file path to a file
            containing raw weather data.
    Returns:
        A string containing the processed and formatted weather data.
    """

    with open(forecast_file) as json_file:
        json_data = json.load(json_file)
        daily_forecast_data = json_data["DailyForecasts"]
        
        overview = generate_overview(daily_forecast_data)
        summary = generate_summary(daily_forecast_data)

        # print(overview)
        # print(summary)

        output = overview + summary

        print(output)

        return output



if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))



# convert_f_to_c(37.0)
# calculate_mean(25, 2)

weather_forecast = process_weather("data/forecast_5days_a.json")
# generate_overview(weather_forecast)
# generate_summary(weather_forecast)

