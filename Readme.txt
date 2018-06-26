
<===========================>
 Infobox v1.5.5 - WeatherApp
<===========================>

Weather GUI displaying time, current weather, 3 and 6 hourly forecast, daytime forecast for next days.

- Get weather infos of your region or even places of other timezones in no time!
  The app is aware of timezones and will display the times of the other timezone for
  current weather and forecasts.

- multilingual support
  (feel free to add more languages in the infobox_languages.py file!
  I wrote sets for English, German and French so far.
  You find a HowTo in the same file.)

- 3 Pages + Settings and Help


Written in Python 3.6.5
tested successfully on Win7 and a RaspberryPi with Raspbian Stretch.
I am sure it will work on MacOS as well.
Created for 3.5inch RPi LCD (A) 320×480 (see some pictures added in the folder).

It's my first code. I started to learn coding with Python this year in February 2018.
I started to write this weather app on 19th of April and it took quite some time to manage the various exceptions
that could rise (i. e. items of JSON data missing, dealing with non-ASCII characters, URLErrors and so on).


=======================
Main file:
infobox_v1.5.5.py
=======================


+++++++++++++
+ You need: +
+++++++++++++

- Python 3 (Maybe Python 2 works, too)

- Some side packages, see 'Modules needed for infobox.txt'

- API key of a free account

  Sign up for free to get API key:
  https://home.openweathermap.org/users/sign_up

  Settings page will open automatically when starting the first time!




Credits:

developed by Jan-Patrick Tyra
https://github.com/jiavu

Ver. 1.5.5 - 26 June 2018


weather data from
https://openweathermap.org/
licence: ODbL

wind vanes by Jan-Patrick Tyra

weather icons by Starder, http://freedesignfile.com
http://freedesignfile.com/204831-vector-weather-icons-design-set-02/

Written in Python 3.6.5