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
    print(total/num_items)
    return int(total / num_items)


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
        return daily_forecast_data

    
def generate_five_day_summary(daily_forecast_data):
    for day in daily_forecast_data:
        iso_date = day["Date"]
        formatted_date = convert_date(iso_date)
        print(formatted_date)

        min_temp_farenheit = day["Temperature"]["Minimum"]["Value"]
        min_temp_celcius = convert_f_to_c(min_temp_farenheit)
        print(min_temp_celcius)

        max_temp_farenheit = day["Temperature"]["Maximum"]["Value"]
        max_temp_celcius = convert_f_to_c(max_temp_farenheit)
        print(max_temp_celcius)

        day_desc = day["Day"]["LongPhrase"]
        print(day_desc)

        night_desc = day["Night"]["LongPhrase"]
        print(night_desc)


# if __name__ == "__main__":
    # print(process_weather("data/forecast_5days_a.json"))



# convert_f_to_c(37.0)
# calculate_mean(25, 2)

weather_forecast = process_weather("data/forecast_5days_a.json")
generate_five_day_summary(weather_forecast)

