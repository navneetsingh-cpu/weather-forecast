import streamlit as st
import requests
import pandas as pd


# Function to convert Celsius to Fahrenheit
def celsius_to_fahrenheit(celsius):
    return (celsius * 9 / 5) + 32


# Function to get weather data from Open-Meteo API
def get_weather_data(city):
    # Replace spaces with '+' symbol for URL encoding
    city = city.replace(" ", "+")

    # Use geocoding to get latitude and longitude for the city
    geocode_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1&language=en&format=json"
    geocode_response = requests.get(geocode_url).json()

    # Extract latitude and longitude from geocode response
    latitude = geocode_response["results"][0]["latitude"]
    longitude = geocode_response["results"][0]["longitude"]

    # Get weather forecast data for the given latitude and longitude
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_min"
    weather_response = requests.get(weather_url).json()
    print(weather_response)
    return weather_response


# Streamlit app
st.title("☀️ Weather Forecast App")

# User input for the city
city = st.text_input("Enter a city name", "Toronto")

if st.button("Show Weather Forecast"):
    # Get weather data
    weather_data = get_weather_data(city)

    if "daily" in weather_data:
        # Convert the hourly data to a DataFrame
        df = pd.DataFrame(weather_data["daily"])

        # Convert temperatures from Celsius to Fahrenheit
        df["temperature_f"] = df["temperature_2m_min"].apply(celsius_to_fahrenheit)

        # new_format = "T%H:%M"
        # df["time"] = d1.strftime(new_format)
        df = df.rename(
            columns={
                "time": "Time",
                "temperature_2m_min": "Temperature (Celsius)",
                "temperature_f": "Temperature (Farenheit)",
            }
        )

        # Display the DataFrame
        st.write(f"Weather forecast today for {city}:")
        st.dataframe(df)

        # Plot a line chart of the temperature over time
        st.line_chart(df[["Time", "Temperature (Celsius)"]].set_index("Time"))
    else:
        st.error("Weather data not found for the specified city.")

# Instructions to run the app
st.sidebar.header("Instructions")
st.sidebar.write(
    """
1. Enter a city name in the input box.
2. Click on 'Show Weather Forecast' to display the weather data.
3. A line chart of the temperature over time will be displayed below the data table.
"""
)
