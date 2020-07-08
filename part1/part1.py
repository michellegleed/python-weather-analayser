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
    """ Generates overview of n number of days in the json data.
    Args:
        daily_forecast_data: the weather data in json format for a given number of days.
    Returns:
        A formatted string.
    """

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

    
def generate_summary(daily_forecast_data):
    """ Generates a daily weather summary for each day in the given weather data.
    Args:
        daily_forecast_data: the weather data in json format for a given number of days.
    Returns:
        A formatted string.
    """

    output = ""

    for day in daily_forecast_data:
        iso_date = day["Date"]
        formatted_date = convert_date(iso_date)

        min_temp_farenheit = day["Temperature"]["Minimum"]["Value"]
        min_temp_celcius = convert_f_to_c(min_temp_farenheit)

        max_temp_farenheit = day["Temperature"]["Maximum"]["Value"]
        max_temp_celcius = convert_f_to_c(max_temp_farenheit)

        day_desc = day["Day"]["LongPhrase"]

        day_rain_probability = day["Day"]["RainProbability"]

        night_desc = day["Night"]["LongPhrase"]

        night_rain_probability = day["Night"]["RainProbability"]

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

        output = overview + summary

        return output


def export_as_text_file(weather_forecast, new_file_path):
    """Exports a pre-generated, pre-formatted weather forecast to a .txt file.

    Args:
        weather_forecast: A formatted string containing the weather report
        new_file_path: A string that represents the destination and name of the new .txt file
    """

    with open(new_file_path, 'w+') as txt_file:
        txt_file.write(weather_forecast)


def prompt_user_to_save(forecast_report):
    """Asks user if they would like to save the weather report as a .txt file using the input() function. If response is "y" then asks for a filename and saves the file to the saved_weather_reports directory.
    """

    export_required = input("Would you like to save this weather report as a .txt file? (Y/N) ")
    if export_required == "y" or export_required == "Y":
        print()
        file_name = input("Enter a name for the file (or leave this empty to cancel the file export) ")
        if file_name != "":
            txt_file_path = f"saved_weather_reports/{file_name}.txt"
            export_as_text_file(forecast_report, txt_file_path)
            print()
            print(f" >> {file_name}.txt was (hopefully) saved to this directory: \n         part1/{txt_file_path}")
            print()
            print()

def choose_weather_report():
    """Asks user which weather report they would like to see. Prints requested report to the console and also returns it.
    """

    print()
    print("Which weather report would you like to see?")
    print()
    print("5 Day Forecast from June 19 (A)")
    print("5 Day Forecast from June 22 (B)")
    print("8 Day Forecast from June 19 (C)")
    print()
    choice = input("Please choose A, B or C.. ")
    print()
    print()

    if choice == "a" or choice =="A":
        return process_weather("data/forecast_5days_a.json")
    elif choice == "b" or choice =="B":
        return process_weather("data/forecast_5days_b.json")
    elif choice == "c" or choice =="C":
        return process_weather("data/forecast_10days.json")
    else:
        print("Sorry, your choice was not a valid option. Printing option A...")
        print()
        return process_weather("data/forecast_5days_a.json")


if __name__ == "__main__":
    print(process_weather("data/forecast_5days_a.json"))


### NOTE: hard-coded function calls for processing and exporting the 5 day (a) weather report...

forecast_report = process_weather("data/forecast_5days_a.json")

# print(forecast_report)

export_as_text_file(forecast_report, "saved_weather_reports/perth_weather_summary.txt")

print(f" >> This weather report has been (hopefully) saved to this directory: \n         part1/saved_weather_reports/perth_weather_summary.txt")


### NOTE: asking for user input to generate the weather reports (commented out so it's quicker for Hayley to run her tests)...

# users_chosen_weather_forecast = choose_weather_report()

# print(users_chosen_weather_forecast)

# prompt_user_to_save(users_chosen_weather_forecast)

print()
print()

