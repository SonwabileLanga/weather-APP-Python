from flask import Flask, render_template, request
import requests
import datetime

app = Flask(__name__)

# OpenWeather API key and URL
OPENWEATHER_API_KEY = '4df0d76850d8b55311fb5c1fc3a90e2c'
OPENWEATHER_API_URL = 'https://api.openweathermap.org/data/2.5/onecall'

# Function to get latitude and longitude for a given city
def get_coordinates(city):
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
    response = requests.get(geo_url)
    if response.status_code == 200:
        data = response.json()
        if data:
            return data[0]['lat'], data[0]['lon']
    return None, None

# Function to convert Unix timestamp to readable date
def unix_to_datetime(unix_timestamp):
    return datetime.datetime.utcfromtimestamp(unix_timestamp).strftime('%A, %d %B')

@app.route('/', methods=['GET', 'POST'])
def index():
    weather_data = {}
    error_message = None

    if request.method == 'POST':
        city = request.form.get('city')

        # Get coordinates for the entered city
        latitude, longitude = get_coordinates(city)

        if latitude and longitude:
            # Get 7-day weather forecast
            response = requests.get(
                f"{OPENWEATHER_API_URL}?lat={latitude}&lon={longitude}&exclude=current,minutely,hourly,alerts&appid={OPENWEATHER_API_KEY}&units=metric"
            )

            if response.status_code == 200:
                weather_data = response.json()
            else:
                error_message = "Failed to fetch weather data from the API."
        else:
            error_message = "City not found. Please check the city name."

    return render_template('index.html', weather_data=weather_data, error_message=error_message, unix_to_datetime=unix_to_datetime)

if __name__ == '__main__':
    app.run(debug=True)
