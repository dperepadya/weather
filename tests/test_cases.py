import unittest
from unittest.mock import patch

import weatherapp
from weatherapp import app


def get_coordinates_mock(*args, **kwargs):
    return {'lat': 10.1, 'lon': -10.1}

def get_weather_data_mock(*args, **kwargs):
    return {
        'latitude': 10.1,
        'longitude': -10.1,
        'temperature': 25.0,
        'wind_speed': 5.0,
        'precipitation': 0.0,
        'location': 'Lat: 10.1, Lon: -10.1'
    }

class TestWeather(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('weatherapp.get_coordinates', get_coordinates_mock)
    def test_get_coordinates(self):
        result = weatherapp.get_coordinates("London")
        expected_data = {'lat': 10.1, 'lon': -10.1}
        self.assertEqual(result, expected_data)

    @patch('weatherapp.get_weather_data', get_weather_data_mock)
    def test_get_weather_data(self):
        coordinates = {'lat': 10.1, 'lon': -10.1}
        result = weatherapp.get_weather_data(coordinates)
        expected_data = {
            'latitude': 10.1,
            'longitude': -10.1,
            'temperature': 25.0,
            'wind_speed': 5.0,
            'precipitation': 0.0,
            'location': 'Lat: 10.1, Lon: -10.1'
        }
        self.assertEqual(result, expected_data)

    @patch('weatherapp.get_weather_data', get_weather_data_mock)
    @patch('weatherapp.get_coordinates', get_coordinates_mock)
    def test_weather_route(self):
        response = self.app.post('/weather', data={'location': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'25.0', response.data)


if __name__ == '__main__':
    unittest.main()