import requests
from datetime import datetime, timedelta
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from urllib.parse import urlparse, parse_qs

# Dictionary to store cached forecasts with zip codes as keys
cache = {}

def get_weather_forecast(zipcode):
    if zipcode in cache and cache[zipcode]['expires_at'] > datetime.now():
        # If forecast is cached and not expired, return cached data
        forecast_data = cache[zipcode]['data']
        from_cache = True
    else:
        # Make API call to fetch weather data
        api_key = '4909bbe3704742deb6294437242903' # Replace with your actual API key
        url = f'http://api.weatherapi.com/v1/current.json?key={api_key}&q={zipcode}&aqi=no'
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            forecast_data = {
                'current_temperature_celcius': data['current']['temp_c'],
                'current_temperature_farenheit': data['current']['temp_f'],
                'humidity': data['current']['humidity'],
                'current_condition': data['current']['condition']['text']
            }
            from_cache = False
            # Cache the forecast for 30 minutes
            expires_at = datetime.now() + timedelta(minutes=30)
            cache[zipcode] = {'data': forecast_data, 'expires_at': expires_at}
        else:
            return None, False  # Failed to fetch data from API

    return forecast_data, from_cache

class WeatherRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        zipcode = query_params.get('zipcode', [None])[0]

        if not zipcode:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Zipcode parameter is required'}).encode('utf-8'))
            return

        forecast_data, from_cache = get_weather_forecast(zipcode)
        if forecast_data:
            forecast_data['from_cache'] = from_cache
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(forecast_data).encode('utf-8'))
        else:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': 'Failed to fetch weather data'}).encode('utf-8'))

def run_server(server_class=HTTPServer, handler_class=WeatherRequestHandler, port=8000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f'Starting server on port {port}...')
    httpd.serve_forever()

run_server()