# JBAD Python project

#### Weather statistics visualization

Artur Sokol

Python used: 3.8

To prepare the environment:

```bash
$ virtualenv -p=/usr/bin/python3.8 jbad-project-env
$ git clone <repo-url>/jbad-project.git
$ cd jbad-project
$ pip install -r requirements.txt
```

---

### API used

1. [Weather API](https://openweathermap.org/);

Parameters meaning:
> Source - OpenWeather history bulk [docs](https://openweathermap.org/history-bulk)

  * `city_name`: city name
  * `lat`: location latitude
  * `lon`: location longitude
  * `main`
    * `main.temp`: temperature
    * `main.feels_like`: this temperature parameter accounts for the human perception of weather
    * `main.pressure`: atmospheric pressure (on the sea level), hPa
    * `main.humidity`: humidity, %
    * `main.temp_min`: minimum temperature at the moment. This is deviation from temperature that is possible for large cities and megalopolises geographically expanded (use these parameter optionally).
    * `main.temp_max`: maximum temperature at the moment. This is deviation from temperature that is possible for large cities and megalopolises geographically expanded (use these parameter optionally).
  * `wind`
    * `wind.speed`: wind speed. Unit Default: meter/sec
    * `wind.deg`: wind direction, degrees (meteorological)
  * `clouds`
    * `clouds.all`: cloudiness, %
  * `rain`
    * `rain.1h`: rain volume for the last hour, mm
    * `rain.3h`: rain volume for the last 3 hours, mm
  * `snow`
    * `snow.1h`: snow volume for the last hour, mm (in liquid state)
    * `snow.3h`: snow volume for the last 3 hours, mm (in liquid state)
  * `weather` (more info Weather condition codes)
    * `weather.id`: weather condition id
    * `weather.main`: group of weather parameters (Rain, Snow, Extreme etc.)
    * `weather.description`: weather condition within the group
    * `weather.icon`: weather icon id
  * `dt`: time of data calculation, unix, UTC
  * `dt_iso`: date and time in UTC format
  * `timezone`: shift in seconds from UTC

---

### Changelog

#### Version 0 (in progress)

* no split on different components, only client is implemented;
* client reads from previously prepared dataset for several regions and supports historical data visualization;
* client is console;
