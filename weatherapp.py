from flask import Flask, render_template, request
import requests

app = Flask(__name__)

GEOCODING_API_URL = "http://api.openweathermap.org/geo/1.0/direct"
WEATHER_API_URL = "https://api.openweathermap.org/data/3.0/onecall"
API_KEY = "your_openweathermap_api_key"
GOOGLE_MAPS_API_KEY = "your_google_maps_api_key"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/weather', methods=['POST'])
def weather():
    location = request.form['location']
    coordinates = get_coordinates(location)
    if coordinates:
        weather_data = get_weather_data(coordinates)
        if weather_data:
            return render_template('map.html', weather_data=weather_data, google_maps_api_key=GOOGLE_MAPS_API_KEY)
    return "Error: Could not retrieve weather data for the specified location."

def get_coordinates(location):
    try:
        response = requests.get(
            GEOCODING_API_URL,
            params={'q': location, 'appid': API_KEY}
        )
        response.raise_for_status()
        data = response.json()
        if data:
            return {'lat': data[0]['lat'], 'lon': data[0]['lon']}
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def get_weather_data(coordinates):
    try:
        response = requests.get(
            WEATHER_API_URL,
            params={
                'lat': coordinates['lat'],
                'lon': coordinates['lon'],
                'appid': API_KEY,
                'units': 'metric'
            }
        )
        response.raise_for_status()
        data = response.json()
        return {
            'latitude': coordinates['lat'],
            'longitude': coordinates['lon'],
            'temperature': data['current']['temp'],
            'wind_speed': data['current']['wind_speed'],
            'precipitation': data['current'].get('rain', {}).get('1h', 0),
            'location': f"Lat: {coordinates['lat']}, Lon: {coordinates['lon']}"
        }
    except requests.RequestException as e:
        print(f"An error occurred: {e}")
        return None

if __name__ == '__main__':
    app.run(debug=True)
