# WeatherAPI Code
 
Welcome to Weather API Code

Please create a python virtual environment to get the supported libraries

```
  cd cloned-directory
  python3 -m venv
  python3 weather_api.py
```

Output

```
147dda08b714:PythonExperiment AwasthiShubham$ python3 weather_api.py 
Starting server on port 8000...
127.0.0.1 - - [01/Apr/2024 10:54:23] "GET / HTTP/1.1" 400 -
127.0.0.1 - - [01/Apr/2024 10:54:23] "GET /favicon.ico HTTP/1.1" 400 -
```
Go to 127.0.0.1/?`zipcode`

If zipcode not entered below error would be thrown

```
{"error": "Zipcode parameter is required"}
```

Sample ZipCode Input and Output
```
Input : http://127.0.0.1:8000/?zipcode=10001
Output
{"current_temperature_celcius": 11.1, "current_temperature_farenheit": 52.0, "humidity": 48, "current_condition": "Partly cloudy", "from_cache": false}

```

If same zipcode is searched again its fethced from cache
```
Input : http://127.0.0.1:8000/?zipcode=10001
Output
{"current_temperature_celcius": 11.1, "current_temperature_farenheit": 52.0, "humidity": 48, "current_condition": "Partly cloudy", "from_cache": true}

```


