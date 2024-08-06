import unittest
from unittest.mock import patch, Mock

import weatherapp
from weatherapp import app


def get_coordinates_mock(location, *args, **kwargs):
    if location == 'London':
        return {'lat': 10.1, 'lon': -10.1}
    return None

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

    @patch('weatherapp.get_coordinates', get_coordinates_mock)
    def test_get_coordinates_failure(self):
        result = weatherapp.get_coordinates("Manchester")
        self.assertIsNone(result)

    @patch('weatherapp.get_coordinates')
    def test_get_coordinates_exception(self, mock_get_coordinates):
        mock_get_coordinates.side_effect = Exception('Cannot get coordinates')
        try:
            result = weatherapp.get_coordinates("London")
        except Exception as e:
            result = None
        self.assertIsNone(result)

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

    @patch('weatherapp.get_weather_data')
    def test_get_weather_data_exception(self, mock_get_weather_data):
        mock_get_weather_data.side_effect = Exception('Cannot get coordinates')
        try:
            coordinates = {'lat': 10.1, 'lon': -10.1}
            result = weatherapp.get_weather_data(coordinates)
        except Exception as e:
            result = None
        self.assertIsNone(result)

    @patch('weatherapp.get_weather_data', get_weather_data_mock)
    @patch('weatherapp.get_coordinates', get_coordinates_mock)
    def test_weather_route(self):
        response = self.app.post('/weather', data={'location': 'London'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'25.0', response.data)

    @patch('weatherapp.get_weather_data', get_weather_data_mock)
    @patch('weatherapp.get_coordinates', get_coordinates_mock)
    def test_weather_route_failure(self):
        response = self.app.post('/weather', data={'location': 'Manchester'})
        self.assertEqual(response.status_code, 404)

    @patch('weatherapp.get_coordinates', Mock(side_effect=Exception('Cannot get coordinates')))
    @patch('weatherapp.get_weather_data', get_weather_data_mock)
    def test_weather_route_exception_coordinates(self):
        response = self.app.post('/weather', data={'location': 'London'})
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Cannot get coordinates')

    @patch('weatherapp.get_coordinates', get_coordinates_mock)
    @patch('weatherapp.get_weather_data', Mock(side_effect=Exception('Cannot get weather data')))
    def test_weather_route_exception_weather(self):
        response = self.app.post('/weather', data={'location': 'London'})
        # print('Response:', response)
        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.get_json()['error'], 'Cannot get weather data')


if __name__ == '__main__':
    unittest.main()
