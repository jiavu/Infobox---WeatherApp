#!/usr/bin/env python3
# Shebang :)
# I tried to make it compatible with Python2 but I think there are some issues with Exception handling.


# hex-valued colors:
# '#%02x%02x%02x' % (R, G, B)  |(?) RGB values are 0 to 256
# tkinter color names: https://wiki.tcl.tk/37701

# Tkinter manual: http://effbot.org/tkinterbook/


try:
	from tkinter import *
	from urllib.request import urlopen
	from urllib import error # I think error.BaseException / error.HTTPError / error.URLError won't work with Python 2. I think it's urllib.requests.exceptions instead of urllib.error in Py2 (?) and Class is RequestException
	from urllib.parse import quote
except ImportError:
	from Tkinter import *
	from urllib2 import urlopen # see above
	from urllib import quote
from os import path
import json, webbrowser
import time as tme
from datetime import datetime, timedelta
from timezonefinder import TimezoneFinder
from pytz import timezone, utc
from PIL import Image, ImageTk

try:
	import infobox_languages
	lang = infobox_languages.lang
	lang_import_failed = False
except:
	print("Import of language package failed."), print()
	lang = {"en":{"hours_minutes":"%I.%M %p","hours_minutes2":"%I.%M %p","hour":":00","weekday_and_date":"{weekday} %d {month} %Y","weekday":{"0":"Sunday","1":"Monday","2":"Tuesday","3":"Wednesday","4":"Thursday","5":"Friday","6":"Saturday","7":"Sunday"},"month":{"01":"January","02":"February","03":"March","04":"April","05":"May","06":"June","07":"July","08":"August","09":"September","10":"October","11":"November","12":"Dezember"},"week_number":"WN {}","wind_direction":{"-":"-","N":"north","NE":"northeast","E":"east","SE":"southeast","S":"south","SW":"southwest","W":"west","NW":"northwest"},"wind_description":{"--":"--","0Bft":"Calm","1Bft":"Light air","2Bft":"Light breeze","3Bft":"Gentle breeze","4Bft":"Moderate breeze","5Bft":"Fresh breeze","6Bft":"Strong breeze","7Bft":"Moderate gale","8Bft":"Fresh gale","9Bft":"Strong gale","10Bft":"Storm","11Bft":"Violent storm","12Bft":"Hurricane"},"wind_format":"{wind_description} from the {wind_direction}","sunrise_sunset":"↑ {}, ↓ {}","clouds":"{}% clouds","clouds2":"{}% clouds","visibility":"{} (km) visibility","temp_rest_day":"Rest of the day: {max}{u} / {min}{u}","humidity":"Humidity: {}%","tomorrow":"Tomorrow:","night":"Night","morning":"Morning","noon":"Noon","evening":"Evening","settings":"Settings","next_page":"Next page","hide_show_b":"Hide/show buttons","fullscreen_onoff":"Fullscreen on/off","fullscreen_esc":"Exit fullscreen","3hourl6hourl":"3 or 6 hourly forecast","help":"Help","reload":"Reload","doubleclick":"Doubleclick","page":"Page ↑ ↓","close":"Close","error":'Error: "',"place_missing":"Please enter a place","api_missing":"Please enter a valid API key","not_found":"Does this place really exist?","unauthorized":"Is your API key correct?","connection":"Am I connected to the internet?","other":"Something went wrong :/","numbers":"Only numbers accepted for City ID","write_save":"Couldn't write save file","cityid":"City ID","timezone":"Timezone","search":"Search","search_by":"Search location by:","get_key":"get a key from\n openweathermap.org","api_key":"API key","city_name":"City name, country code","zip":"ZIP, country code","auto":"Automatically (IP)"}}
	lang_import_failed = True
	

infobox_version = "1.5.5"
release_date = "26 June 2018"
set_font = "Carlito" 							# On my RaspberryPi the font is to large for a long weather description, i. e. "Thunderstorm with heavy drizzle" wouldn't be displayed completely.
main_bg_color = "black" 	 # Background color
main_fg_color = "light grey" # Color of font
clock_color = "turquoise"


file_location = path.dirname(path.realpath(__file__))
img_dir = file_location + "/Images/"
file_strich= img_dir + "strich_v2_75p.gif"
file_strich2= img_dir + "strich_v3.gif"
file_strich3= img_dir + "strich_v4.gif"
saved_settings = file_location + "/" + "saved_settings.txt"

utc = timezone("utc") # Don't edit!



class Uhr:
	def __init__(self):
		self.strich = PhotoImage(file=file_strich)
		self.strich2 = PhotoImage(file=file_strich2)
		self.frame0 = Frame(window)
		
		self.std_min = "--:--"
		self.sec = "--"
		self.date = "-- month ----"
		self.kw = "--"
		
		self.layout1()
		self.update_import_data()
		
	def layout1(self):
		self.frame0.place_forget()
				
		self.frame0 = Frame(window, bg=main_bg_color)
		self.frame1 = Frame(self.frame0, bg=main_bg_color)
		self.frame2 = Frame(self.frame0, bg=main_bg_color)

		self.disp_std_min = Label(self.frame1,
                    font= set_font + " 22",
                    fg= clock_color,
					bg=main_bg_color)
		self.disp_sec = Label(self.frame1,
                    font= set_font + " 11",
                    fg=main_fg_color,
                    bg=main_bg_color)
		"""
		self.disp_line = Label(self.frame0,
					#text="----",
					image=self.strich,
					bg=main_bg_color,
					fg="white")
		"""
		self.disp_line2 = Label(window,
					#text="----",
					image=self.strich2,
					bg=main_bg_color,
					fg="white")
		self.disp_date = Label(self.frame2,
                    font= set_font + " 10",
                    fg=main_fg_color,
                    bg=main_bg_color)
		self.disp_kw = Label(self.frame2,
					font= set_font + " 7",
					fg=main_fg_color,
					bg=main_bg_color)

		self.frame0.place(relx=0.5, rely=0.5, width= 400, height=100, anchor=S)
		self.frame1.place(relx=0.5, rely=0.5, y=5, anchor=S)
		self.frame2.place(relx=0.5, rely=0.5, y=1, anchor=N)
		
		self.update_widgets()
		
		self.disp_std_min.pack(side="left") #, expand=True)
		self.disp_sec.pack(side="left")     #, expand=1)
		self.disp_date.pack()				#, expand=YES)
		self.disp_kw.pack()
		#self.disp_line.place(relx=0.5, rely=0.5, anchor=CENTER)
		self.disp_line2.place(relx=0.5, rely=0.5, anchor=S)
		
	def layout2(self):
		self.frame0.place_forget()
		self.disp_line2.place_forget()
		self.update_widgets()
		
		self.frame0 = Frame(window, bg=main_bg_color)
		self.frame1 = Frame(self.frame0, bg=main_bg_color)
		
		self.disp_std_min = Label(self.frame0,
                    font= set_font + " 10",
                    fg="turquoise",
					bg=main_bg_color)
		self.disp_sec = Label(self.frame0,
                    font= set_font + " 10",
                    fg=main_fg_color,
                    bg=main_bg_color)
		"""
		self.disp_line = Label(self.frame0,
					#text="----",
					image=self.strich,
					bg=main_bg_color,
					fg="white")
		"""
		self.disp_line2 = Label(self.frame0,
					#text="----",
					image=self.strich2,
					bg=main_bg_color,
					fg="white")
		self.disp_date = Label(self.frame0,
                    font= set_font + " 10",
                    fg=main_fg_color,
                    bg=main_bg_color)
		self.disp_kw = Label(self.frame0,
					font= set_font + " 7",
					fg=main_fg_color,
					bg=main_bg_color)

		self.frame0.place(relx=0.5, rely=0.5, height=25, x=-220, y=-150, anchor=NW) # width= 220
		#self.frame1.place(relx=0, rely=0, anchor=NW)

		self.update_widgets()
		
		self.disp_date.pack(side="left")
		self.disp_std_min.pack(side="left")
		#self.disp_sec.pack(side="left")
		#self.disp_line.place(relx=0.5, rely=0.5, anchor=CENTER)
		self.disp_line2.place(relx=0, rely=1, y=+1, anchor=SW)
		#self.disp_line2.lift(self.frame0)
	
	def update_import_data(self):
		weekday = lang[my_language]["weekday"][tme.strftime("%w")]
		month = lang[my_language]["month"][tme.strftime("%m")]
		self.std_min = tme.strftime(lang[my_language]["hours_minutes"])
		self.sec = tme.strftime("%S")
		self.date = tme.strftime(lang[my_language]["weekday_and_date"].format(weekday=weekday, month=month))
		#self.date = "Donnerstag, 29. September 2020"
		self.kw = lang[my_language]["week_number"].format(tme.strftime("%W"))
		
		self.update_widgets()
		self.frame0.after(50, self.update_import_data) # => 50ms update intervall. Maybe 200 ms is fast enough. Could a low update intervall cause problems?
		
	def update_widgets(self):
		self.disp_std_min.config(text=self.std_min)
		self.disp_sec.configure(text=self.sec)
		self.disp_date.config(text=self.date)
		self.disp_kw.config(text=self.kw)



class WeatherApp:

	def __init__(self):
		
		global hf
		hf = False
		
		self.strich = PhotoImage(file=file_strich3)
		
		self.c_iconid = "00x"
		self.c_icon = PhotoImage(file=img_dir + self.c_iconid + ".png")

		self.c_dt = "--:--"
		self.c_dt_intimezone = "--:-- Uhr"
		self.c_timezone = "tz n.a."
		self.c_zone_timezone = ""
		self.c_lon = ""
		self.c_lat = ""
		self.c_locname = "no info" # Location name could be up to 34 chars long
		self.c_cityid = ""
		self.c_temp = "--.-"
		self.c_humidity = "--"
		self.c_pressure = "----.-"
		self.c_description = "no info" # Replace for adjusting: "Thunderstorm with heavy drizzle" #"Gewitter mit starkem Nieselregen" #Lorem ipsum dolor sit amet, in"
		self.c_windspeed = "--.--"
		self.c_winddeg = None
		self.c_windvane_id = "noinfo"
		self.c_windvane = PhotoImage(file=img_dir + self.c_windvane_id + ".png")
		self.c_sunset = "--:--"
		self.c_sunrise = "--:--"
		self.c_country = "Lorem"
		self.c_clouds = "--"
		self.c_rain = "-"
		self.c_visibility = "--"
		
		self.c_temp_min = "--"
		self.c_temp_max = "--"

		self.n1_time = 0
		self.n1_temp = "--"
		self.n1_iconid = "00x"
		self.n1_icon = PhotoImage(file=img_dir + self.n1_iconid + ".png")
		self.n1_description = "no info"
		self.n1_clouds = "--"
		self.n1_windspeed = "-.--"
		self.n1_winddeg = None
		self.n1_windvane_id = "noinfo"
		self.n1_windvane = PhotoImage(file=img_dir + self.n1_windvane_id + ".png")
			
		self.n2_time = 0
		self.n2_temp = "--"
		self.n2_iconid = "00x"
		self.n2_icon = PhotoImage(file=img_dir + self.n2_iconid + ".png")
		self.n2_description = "no info"
		self.n2_clouds = "--"
		self.n2_windspeed = "-.--"
		self.n2_winddeg = None
		self.n2_windvane_id = "noinfo"
		self.n2_windvane = PhotoImage(file=img_dir + self.n2_windvane_id + ".png")

		self.n3_time = 0
		self.n3_day = None
		self.n3_temp = "--"
		self.n3_iconid = "00x"
		self.n3_icon = PhotoImage(file=img_dir + self.n3_iconid + ".png")		
		self.n3_description = "no info"
		self.n3_clouds = "--"
		self.n3_windspeed = "-.--"
		self.n3_winddeg = None
		self.n3_windvane_id = "noinfo"
		self.n3_windvane = PhotoImage(file=img_dir + self.n3_windvane_id + ".png")
		
		self.n1_a_time = 0
		self.n1_a_temp = "--"
		self.n1_a_iconid = "00x"
		self.n1_a_description = "no info"
		self.n1_a_clouds = "--"
		self.n1_a_windspeed = "-.--"
		self.n1_a_winddeg = None
		self.n2_a_time = 0
		self.n2_a_temp = "--"
		self.n2_a_iconid = "00x"
		self.n2_a_description = "no info"
		self.n2_a_clouds = "--"
		self.n2_a_windspeed = "-.--"
		self.n2_a_winddeg = None
		self.n3_a_time = 0
		self.n3_a_temp = "--"
		self.n3_a_iconid = "00x"
		self.n3_a_description = "no info"
		self.n3_a_clouds = "--"
		self.n3_a_windspeed = "-.--"
		self.n3_a_winddeg = None
		
		self.n1_b_time = 0
		self.n1_b_temp = "--"
		self.n1_b_iconid = "00x"
		self.n1_b_description = "no info"
		self.n1_b_clouds = "--"
		self.n1_b_windspeed = "-.--"
		self.n1_b_winddeg = None
		self.n2_b_time = 0
		self.n2_b_temp = "--"
		self.n2_b_iconid = "00x"
		self.n2_b_description = "no info"
		self.n2_b_clouds = "--"
		self.n2_b_windspeed = "-.--"
		self.n2_b_winddeg = None
		self.n3_b_time = 0
		self.n3_b_temp = "--"
		self.n3_b_iconid = "00x"
		self.n3_b_description = "no info"
		self.n3_b_clouds = "--"
		self.n3_b_windspeed = "-.--"
		self.n3_b_winddeg = None
		
		self.nday1_temp_min = "--"
		self.nday1_temp_max = "--"
		self.nday1 = "Tomorrow:"
				
		self.nday1_night_iconid = "00x"
		self.nday1_night_icon = PhotoImage(file=img_dir + self.nday1_night_iconid + ".png")
		self.nday1_night_temp = "--"
		self.nday1_night_windspeed = "-.--"
		self.nday1_night_winddeg = None
		self.nday1_night_windvane_id = "noinfo"
		self.nday1_night_windvane = PhotoImage(file=img_dir + self.nday1_night_windvane_id + ".png")
		
		self.nday1_morning_iconid = "00x"
		self.nday1_morning_icon = PhotoImage(file=img_dir + self.nday1_morning_iconid + ".png")
		self.nday1_morning_temp = "--"
		self.nday1_morning_windspeed = "-.--"
		self.nday1_morning_winddeg = None
		self.nday1_morning_windvane_id = "noinfo"
		self.nday1_morning_windvane = PhotoImage(file=img_dir + self.nday1_morning_windvane_id + ".png")
		
		self.nday1_noon_iconid = "00x"
		self.nday1_noon_icon = PhotoImage(file=img_dir + self.nday1_noon_iconid + ".png")
		self.nday1_noon_temp = "--"
		self.nday1_noon_windspeed = "-.--"
		self.nday1_noon_winddeg = None
		self.nday1_noon_windvane_id = "noinfo"
		self.nday1_noon_windvane = PhotoImage(file=img_dir + self.nday1_noon_windvane_id + ".png")
		
		self.nday1_evening_iconid = "00x"
		self.nday1_evening_icon = PhotoImage(file=img_dir + self.nday1_evening_iconid + ".png")
		self.nday1_evening_temp = "--"
		self.nday1_evening_windspeed = "-.--"
		self.nday1_evening_winddeg = None
		self.nday1_evening_windvane_id = "noinfo"
		self.nday1_evening_windvane = PhotoImage(file=img_dir + self.nday1_evening_windvane_id + ".png")

		
		self.nday2_temp_min = "--"
		self.nday2_temp_max = "--"
		self.nday2 = "Day:"
		
		self.nday2_night_iconid = "00x"
		self.nday2_night_icon = PhotoImage(file=img_dir + self.nday2_night_iconid + ".png")
		self.nday2_night_temp = "--"
		self.nday2_night_windspeed = "-.--"
		self.nday2_night_winddeg = None
		self.nday2_night_windvane_id = "noinfo"
		self.nday2_night_windvane = PhotoImage(file=img_dir + self.nday2_night_windvane_id + ".png")
		
		self.nday2_morning_iconid = "00x"
		self.nday2_morning_icon = PhotoImage(file=img_dir + self.nday2_morning_iconid + ".png")
		self.nday2_morning_temp = "--"
		self.nday2_morning_windspeed = "-.--"
		self.nday2_morning_winddeg = None
		self.nday2_morning_windvane_id = "noinfo"
		self.nday2_morning_windvane = PhotoImage(file=img_dir + self.nday2_morning_windvane_id + ".png")
		
		self.nday2_noon_iconid = "00x"
		self.nday2_noon_icon = PhotoImage(file=img_dir + self.nday2_noon_iconid + ".png")
		#self.nday2_noon_icon = Image.open(img_dir + self.nday2_noon_iconid + ".png")
		self.nday2_noon_temp = "--"
		self.nday2_noon_windspeed = "-.--"
		self.nday2_noon_winddeg = None
		self.nday2_noon_windvane_id = "noinfo"
		self.nday2_noon_windvane = PhotoImage(file=img_dir + self.nday2_noon_windvane_id + ".png")
		
		self.nday2_evening_iconid = "00x"
		self.nday2_evening_icon = PhotoImage(file=img_dir + self.nday2_evening_iconid + ".png")
		self.nday2_evening_temp = "--"
		self.nday2_evening_windspeed = "-.--"
		self.nday2_evening_winddeg = None
		self.nday2_evening_windvane_id = "noinfo"
		self.nday2_evening_windvane = PhotoImage(file=img_dir + self.nday2_evening_windvane_id + ".png")

		
		self.nday3_temp_min = "--"
		self.nday3_temp_max = "--"
		self.nday3_iconid = "00x"
		self.nday3_icon = PhotoImage(file=img_dir + self.nday3_iconid + ".png")
		self.nday3 = "Day:"
		
		self.nday3_night_iconid = "00x"
		self.nday3_night_icon = PhotoImage(file=img_dir + self.nday3_night_iconid + ".png")
		self.nday3_night_temp = "--"
		self.nday3_night_windspeed = "-.--"
		self.nday3_night_winddeg = None
		self.nday3_night_windvane_id = "noinfo"
		self.nday3_night_windvane = PhotoImage(file=img_dir + self.nday3_night_windvane_id + ".png")
		
		self.nday3_morning_iconid = "00x"
		self.nday3_morning_icon = PhotoImage(file=img_dir + self.nday3_morning_iconid + ".png")
		self.nday3_morning_temp = "--"
		self.nday3_morning_windspeed = "-.--"
		self.nday3_morning_winddeg = None
		self.nday3_morning_windvane_id = "noinfo"
		self.nday3_morning_windvane = PhotoImage(file=img_dir + self.nday3_morning_windvane_id + ".png")
		
		self.nday3_noon_iconid = "00x"
		self.nday3_noon_icon = PhotoImage(file=img_dir + self.nday3_noon_iconid + ".png")
		self.nday3_noon_temp = "--"
		self.nday3_noon_windspeed = "-.--"
		self.nday3_noon_winddeg = None
		self.nday3_noon_windvane_id = "noinfo"
		self.nday3_noon_windvane = PhotoImage(file=img_dir + self.nday3_noon_windvane_id + ".png")
		
		self.nday3_evening_iconid = "00x"
		self.nday3_evening_icon = PhotoImage(file=img_dir + self.nday3_evening_iconid + ".png")
		self.nday3_evening_temp = "--"
		self.nday3_evening_windspeed = "-.--"
		self.nday3_evening_winddeg = None
		self.nday3_evening_windvane_id = "noinfo"
		self.nday3_evening_windvane = PhotoImage(file=img_dir + self.nday3_evening_windvane_id + ".png")
		
		self.button_switch_hf3_file = Image.open(img_dir + "Buttons/switch_hf3.png")
		self.button_switch_hf3_file = self.button_switch_hf3_file.resize((32,32), Image.ANTIALIAS)
		self.button_switch_hf3_file = ImageTk.PhotoImage(self.button_switch_hf3_file)
		self.button_switch_hf6_file = Image.open(img_dir + "Buttons/switch_hf6.png")
		self.button_switch_hf6_file = self.button_switch_hf6_file.resize((32,32), Image.ANTIALIAS)
		self.button_switch_hf6_file = ImageTk.PhotoImage(self.button_switch_hf6_file)
		
		
		self.frame0 = Frame(window)
		
		self.layout1()
		self.update_data()
		
	
	def layout1(self):
	
		"""
		CURRENT:
		- Temperatur
		- Icon
		- Weather condition (Description)
		- Windbeschreibung, Windgeschwindigkeit, Windrichtung als Code(N) (Beschreibung wäre im XML-Datensatz..)
		- Sonnenaufgang, Sonnenuntergang (Umwandeln: Time of data calculation, unix, UTC)
		"""
		self.frame0.place_forget()
		
		# Frames definieren:
		self.frame0 = Frame(window, bg=main_bg_color)
		self.frame_current = Frame(self.frame0, bg=main_bg_color) #relief? flat/sunken/raised/groove/RIDGE +borderwidth
		self.frame_info1 = Frame(self.frame0, bg=main_bg_color)
		self.frame_forecasts = Frame(self.frame0)
		#self.frame_next1 = Frame(self.frame0)
		#self.frame_next2 = Frame(self.frame0)
		#self.frame_next3 = Frame(self.frame0)
		self.frame_nextdays = Frame(self.frame0)
		#self.frame_nextday2 = Frame(self.frame0)
		#self.frame_nextday3 = Frame(self.frame0)
		
		# Place Frames:
		self.frame0.place(relx=0.5, rely=0.5, width=400, height=140, anchor=N)
		self.frame_current.place(y=+8, relx=0.43, rely=0, relwidth=0.25, relheight=1, anchor=NE)
		self.frame_info1.place(y=+32, relx=0.43, rely=0, relwidth=0.5, width=+30, relheight=1, anchor=NW)
		
		# Define Labels:
		self.import_state = Label(self.frame0, font="Arial 7", fg="red4", bg=main_bg_color)
		
		
		self.curr_dt = Label(self.frame_info1, font="Arial 7", fg="grey", bg=main_bg_color)
		self.curr_temp = Label(self.frame_current, font=set_font+" 16", fg=main_fg_color, bg=main_bg_color)
		self.curr_icon = Label(self.frame_current, bg=main_bg_color, image=self.c_icon)
		self.curr_description = Label(self.frame_info1, font=set_font+" 11", fg=main_fg_color, bg=main_bg_color,)
		self.curr_wind = Label(self.frame_info1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		self.curr_sun = Label(self.frame_info1, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color)

		# These Labels are not displayed in Layout1 but they need to exist before self.update_widgets
		self.curr_dt_intimezone = Label(self.frame0)
		self.curr_timezone = Label(self.frame0)
		self.curr_locname = Label(self.frame_info1)
		self.curr_infolabel = Label(self.frame_info1)
		self.curr_windvane = Label(self.frame0)
		#self.curr_pressure = Label(self.frame_current)

		
		# Forecast Labels		
		self.next1_time = Label(self.frame_forecasts)
		self.next1_temp = Label(self.frame_forecasts)
		self.next1_icon = Label(self.frame_forecasts)
		#self.next1_description = Label(self.frame_next1)
		#self.next1_clouds = Label(self.frame_next1)
		#self.next1_wind = Label(self.frame_next1)
		self.next1_windvane = Label(self.frame_forecasts)
		self.next1_infolabel = Label(self.frame_forecasts)
		
		self.next2_time = Label(self.frame_forecasts)
		self.next2_temp = Label(self.frame_forecasts)
		self.next2_icon = Label(self.frame_forecasts)
		#self.next2_description = Label(self.frame_next2)
		#self.next2_clouds = Label(self.frame_next2)
		#self.next2_wind = Label(self.frame_next2)
		self.next2_windvane = Label(self.frame_forecasts)
		self.next2_infolabel = Label(self.frame_forecasts)

		self.next3_time = Label(self.frame_forecasts)
		self.next3_temp = Label(self.frame_forecasts)
		self.next3_icon = Label(self.frame_forecasts)
		#self.next3_description = Label(self.frame_next3)
		#self.next3_clouds = Label(self.frame_next3)
		#self.next3_wind = Label(self.frame_next3)
		self.next3_windvane = Label(self.frame_forecasts)
		self.next3_infolabel = Label(self.frame_forecasts)
		
		
		#Labels Nextday
		self.nextday = Label(self.frame_nextdays)
		self.nextday_icon = Label(self.frame_nextdays)
		self.nextday_temp1 = Label(self.frame_nextdays)
		self.nextday_temp2 = Label(self.frame_nextdays)
		
		# Labels Nextday with daytime
		self.nextday1 = Label(self.frame_nextdays)
		self.nextday1_temp1 = Label(self.frame_nextdays)
		self.nextday1_temp2 = Label(self.frame_nextdays)
		self.nextday1_night_temp = Label(self.frame_nextdays)
		self.nextday1_night_icon = Label(self.frame_nextdays)
		self.nextday1_night_windvane = Label(self.frame_nextdays)
		self.nextday1_night_infolabel = Label(self.frame_nextdays)
		self.nextday1_morning_temp = Label(self.frame_nextdays)
		self.nextday1_morning_icon = Label(self.frame_nextdays)
		self.nextday1_morning_windvane = Label(self.frame_nextdays)
		self.nextday1_morning_infolabel = Label(self.frame_nextdays)
		self.nextday1_noon_temp = Label(self.frame_nextdays)
		self.nextday1_noon_icon = Label(self.frame_nextdays)
		self.nextday1_noon_windvane = Label(self.frame_nextdays)
		self.nextday1_noon_infolabel = Label(self.frame_nextdays)
		self.nextday1_evening_temp = Label(self.frame_nextdays)
		self.nextday1_evening_icon = Label(self.frame_nextdays)
		self.nextday1_evening_windvane = Label(self.frame_nextdays)
		self.nextday1_evening_infolabel = Label(self.frame_nextdays)
		
		self.nextday2 = Label(self.frame_nextdays)
		self.nextday2_temp1 = Label(self.frame_nextdays)
		self.nextday2_temp2 = Label(self.frame_nextdays)
		self.nextday2_night_temp = Label(self.frame_nextdays)
		self.nextday2_night_icon = Label(self.frame_nextdays)
		self.nextday2_night_windvane = Label(self.frame_nextdays)
		self.nextday2_night_infolabel = Label(self.frame_nextdays)
		self.nextday2_morning_temp = Label(self.frame_nextdays)
		self.nextday2_morning_icon = Label(self.frame_nextdays)
		self.nextday2_morning_windvane = Label(self.frame_nextdays)
		self.nextday2_morning_infolabel = Label(self.frame_nextdays)
		self.nextday2_noon_temp = Label(self.frame_nextdays)
		self.nextday2_noon_icon = Label(self.frame_nextdays)
		self.nextday2_noon_windvane = Label(self.frame_nextdays)
		self.nextday2_noon_infolabel = Label(self.frame_nextdays)
		self.nextday2_evening_temp = Label(self.frame_nextdays)
		self.nextday2_evening_icon = Label(self.frame_nextdays)
		self.nextday2_evening_windvane = Label(self.frame_nextdays)
		self.nextday2_evening_infolabel = Label(self.frame_nextdays)
		
		self.nextday3 = Label(self.frame_nextdays)
		self.nextday3_temp1 = Label(self.frame_nextdays)
		self.nextday3_temp2 = Label(self.frame_nextdays)
		self.nextday3_night_temp = Label(self.frame_nextdays)
		self.nextday3_night_icon = Label(self.frame_nextdays)
		self.nextday3_night_windvane = Label(self.frame_nextdays)
		self.nextday3_night_infolabel = Label(self.frame_nextdays)
		self.nextday3_morning_temp = Label(self.frame_nextdays)
		self.nextday3_morning_icon = Label(self.frame_nextdays)
		self.nextday3_morning_windvane = Label(self.frame_nextdays)
		self.nextday3_morning_infolabel = Label(self.frame_nextdays)
		self.nextday3_noon_temp = Label(self.frame_nextdays)
		self.nextday3_noon_icon = Label(self.frame_nextdays)
		self.nextday3_noon_windvane = Label(self.frame_nextdays)
		self.nextday3_noon_infolabel = Label(self.frame_nextdays)
		self.nextday3_evening_temp = Label(self.frame_nextdays)
		self.nextday3_evening_icon = Label(self.frame_nextdays)
		self.nextday3_evening_windvane = Label(self.frame_nextdays)
		self.nextday3_evening_infolabel = Label(self.frame_nextdays)
		
		self.button_switch_hf = Label(self.frame0)
		
		
		self.update_widgets()
		
		# Place Labels:
		self.curr_temp.pack()
		self.curr_icon.pack()
		self.curr_description.pack(anchor=W)
		self.curr_wind.pack(anchor=W)
		self.curr_sun.pack(anchor=W)
		self.curr_dt.pack(padx=40, anchor=SE)
		self.import_state.place(relx=1, rely=1, x=-3, y=-25, anchor=SE)

	
	def layout2(self):
	
		self.frame0.place_forget()
		
		# Define Frames:
		self.frame0 = Frame(window, bg=main_bg_color)
		self.frame_current = Frame(self.frame0, bg=main_bg_color) #relief? flat/sunken/raised/groove/RIDGE +borderwidth
		self.frame_info1 = Frame(self.frame0, bg=main_bg_color, borderwidth=1, relief="ridge")
		self.frame_forecasts = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="groove")
		#self.frame_next1 = Frame(self.frame0, bg="green")#, borderwidth=1, relief="ridge")
		#self.frame_next2 = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="ridge")
		#self.frame_next3 = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="ridge")
		self.frame_nextdays = Frame(self.frame0, bg=main_bg_color)
		#self.frame_nextday2 = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="ridge")
		#self.frame_nextday3 = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="ridge")
		

		# Place Frames:
		self.frame0.place(relx=0.5, rely=0.5, width=440, height=255, y=-115, anchor=N)
		self.frame_current.place(relx=0, rely=0.33, relwidth=0.25, relheight=0.33, anchor=SW)
		self.frame_info1.place(relx=0, rely=0.33, y=+2, relwidth=0.5, relheight=0.57, anchor=NW)
		self.frame_forecasts.place(relx=1, rely=0.05, relwidth=0.47, relheight=0.68, anchor=NE)
		#self.frame_next1.place(relx=0.25, rely=0.5, relwidth=0.25, relheight=0.5, anchor=NW)
		#self.frame_next2.place(relx=0.5, rely=0, relwidth=0.25, relheight=0.5, anchor=NW)
		#self.frame_next3.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.5, anchor=NW)
		self.frame_nextdays.place(relx=1, rely=0.755, relwidth=0.47, anchor=NE) #relheight=0.262 für einen Abstand von 0.05 nach unten
		#self.frame_nextday2.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=0.5, anchor=NW)
		#self.frame_nextday3.place(relx=0.75, rely=0.5, relwidth=0.25, relheight=0.5, anchor=NW)
				
		self.disp_line = Label(self.frame0, image=self.strich, bg=main_bg_color)
		self.disp_line.place(relx=0.53, rely=0.7325, anchor=W) # rely=0.7425 ' rely=0.735
		
		
		# Define Labels:
		self.import_state = Label(self.frame0, font="Arial 7", fg="red4", bg=main_bg_color)
		
		self.curr_dt = Label(self.frame0, font="Arial 7", fg="grey", bg=main_bg_color, relief="ridge", borderwidth=1) # oder groove?
		self.curr_dt_intimezone = Label(self.frame0, font="Arial 8", fg=main_fg_color, bg=main_bg_color)
		self.curr_timezone = Label(self.frame0, font="Arial 7", fg="grey", bg=main_bg_color)
		self.curr_temp = Label(self.frame_current, font=set_font+" 16", fg=main_fg_color, bg=main_bg_color)
		self.curr_icon = Label(self.frame_current, bg=main_bg_color, image=self.c_icon)
		self.curr_windvane = Label(self.frame0, bg=main_bg_color, image=self.c_windvane)
		self.curr_description = Label(self.frame_info1, font=set_font+" 11", fg=main_fg_color, bg=main_bg_color)
		self.curr_wind = Label(self.frame_info1, font=set_font+" 9", fg=main_fg_color, bg=main_bg_color)
		self.curr_sun = Label(self.frame_info1, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color)
		self.curr_locname = Label(self.frame_info1, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color)
		self.curr_infolabel = Label(self.frame_info1, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color, justify=LEFT)		
		#self.curr_pressure = Label(self.frame_current, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color, text="Luftdruck: "+"xxxx"+" hpa")
		
		
		#Labels hourly-forecasts
		self.next1_time = Label(self.frame_forecasts, font=(set_font, 8), fg=main_fg_color, bg=main_bg_color)
		self.next1_temp = Label(self.frame_forecasts, font=set_font+" 13", fg=main_fg_color, bg=main_bg_color)
		self.next1_icon = Label(self.frame_forecasts, bg=main_bg_color, image=self.n1_icon)
		#self.next1_description = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next1_clouds = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next1_wind = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		self.next1_windvane = Label(self.frame_forecasts, bg=main_bg_color, image=self.n1_windvane)
		self.next1_infolabel = Label(self.frame_forecasts, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		
		self.next2_time = Label(self.frame_forecasts, font=(set_font, 8), fg=main_fg_color, bg=main_bg_color)
		self.next2_temp = Label(self.frame_forecasts, font=set_font+" 13", fg=main_fg_color, bg=main_bg_color)
		self.next2_icon = Label(self.frame_forecasts, bg=main_bg_color, image=self.n2_icon)
		#self.next2_description = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next2_clouds = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next2_wind = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		self.next2_windvane = Label(self.frame_forecasts, bg=main_bg_color, image=self.n2_windvane)
		self.next2_infolabel = Label(self.frame_forecasts, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)

		self.next3_time = Label(self.frame_forecasts, font=(set_font, 8), fg=main_fg_color, bg=main_bg_color)
		self.next3_temp = Label(self.frame_forecasts, font=set_font+" 13", fg=main_fg_color, bg=main_bg_color)
		self.next3_icon = Label(self.frame_forecasts, bg=main_bg_color, image=self.n3_icon)
		#self.next3_description = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next3_clouds = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next3_wind = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		self.next3_windvane = Label(self.frame_forecasts, bg=main_bg_color, image=self.n3_windvane)
		self.next3_infolabel = Label(self.frame_forecasts, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		
		
		#Labels Nextday
		self.nextday = Label(self.frame_nextdays, font=(set_font, 8, "bold"), fg=main_fg_color, bg=main_bg_color)
		self.nextday_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_noon_icon)
		self.nextday_temp1 = Label(self.frame_nextdays, font=set_font+" 12", fg=main_fg_color, bg=main_bg_color)
		self.nextday_temp2 = Label(self.frame_nextdays, font=set_font+" 12", fg="grey", bg=main_bg_color)
		
		# Labels Nextday with daytime
		self.nextday1 = Label(self.frame_nextdays)
		self.nextday1_temp1 = Label(self.frame_nextdays)
		self.nextday1_temp2 = Label(self.frame_nextdays)
		self.nextday1_night_temp = Label(self.frame_nextdays)
		self.nextday1_night_icon = Label(self.frame_nextdays)
		self.nextday1_night_windvane = Label(self.frame_nextdays)
		self.nextday1_night_infolabel = Label(self.frame_nextdays)
		self.nextday1_morning_temp = Label(self.frame_nextdays)
		self.nextday1_morning_icon = Label(self.frame_nextdays)
		self.nextday1_morning_windvane = Label(self.frame_nextdays)
		self.nextday1_morning_infolabel = Label(self.frame_nextdays)
		self.nextday1_noon_temp = Label(self.frame_nextdays)
		self.nextday1_noon_icon = Label(self.frame_nextdays)
		self.nextday1_noon_windvane = Label(self.frame_nextdays)
		self.nextday1_noon_infolabel = Label(self.frame_nextdays)
		self.nextday1_evening_temp = Label(self.frame_nextdays)
		self.nextday1_evening_icon = Label(self.frame_nextdays)
		self.nextday1_evening_windvane = Label(self.frame_nextdays)
		self.nextday1_evening_infolabel = Label(self.frame_nextdays)
		
		self.nextday2 = Label(self.frame_nextdays)
		self.nextday2_temp1 = Label(self.frame_nextdays)
		self.nextday2_temp2 = Label(self.frame_nextdays)
		self.nextday2_night_temp = Label(self.frame_nextdays)
		self.nextday2_night_icon = Label(self.frame_nextdays)
		self.nextday2_night_windvane = Label(self.frame_nextdays)
		self.nextday2_night_infolabel = Label(self.frame_nextdays)
		self.nextday2_morning_temp = Label(self.frame_nextdays)
		self.nextday2_morning_icon = Label(self.frame_nextdays)
		self.nextday2_morning_windvane = Label(self.frame_nextdays)
		self.nextday2_morning_infolabel = Label(self.frame_nextdays)
		self.nextday2_noon_temp = Label(self.frame_nextdays)
		self.nextday2_noon_icon = Label(self.frame_nextdays)
		self.nextday2_noon_windvane = Label(self.frame_nextdays)
		self.nextday2_noon_infolabel = Label(self.frame_nextdays)
		self.nextday2_evening_temp = Label(self.frame_nextdays)
		self.nextday2_evening_icon = Label(self.frame_nextdays)
		self.nextday2_evening_windvane = Label(self.frame_nextdays)
		self.nextday2_evening_infolabel = Label(self.frame_nextdays)
		
		self.nextday3 = Label(self.frame_nextdays)
		self.nextday3_temp1 = Label(self.frame_nextdays)
		self.nextday3_temp2 = Label(self.frame_nextdays)
		self.nextday3_night_temp = Label(self.frame_nextdays)
		self.nextday3_night_icon = Label(self.frame_nextdays)
		self.nextday3_night_windvane = Label(self.frame_nextdays)
		self.nextday3_night_infolabel = Label(self.frame_nextdays)
		self.nextday3_morning_temp = Label(self.frame_nextdays)
		self.nextday3_morning_icon = Label(self.frame_nextdays)
		self.nextday3_morning_windvane = Label(self.frame_nextdays)
		self.nextday3_morning_infolabel = Label(self.frame_nextdays)
		self.nextday3_noon_temp = Label(self.frame_nextdays)
		self.nextday3_noon_icon = Label(self.frame_nextdays)
		self.nextday3_noon_windvane = Label(self.frame_nextdays)
		self.nextday3_noon_infolabel = Label(self.frame_nextdays)
		self.nextday3_evening_temp = Label(self.frame_nextdays)
		self.nextday3_evening_icon = Label(self.frame_nextdays)
		self.nextday3_evening_windvane = Label(self.frame_nextdays)
		self.nextday3_evening_infolabel = Label(self.frame_nextdays)
		
		self.button_switch_hf = Label(self.frame0, bg=main_bg_color, cursor="hand2")
		
		
		self.update_widgets()
		
		
		# Place Labels:
		self.import_state.place(relx=0.5, rely=1, x=-30, anchor=SE)
		self.curr_dt.place(relx=0.5, rely=1, anchor=SE)
		self.curr_dt_intimezone.place(relx=0, rely=1, anchor=SW)
		self.curr_timezone.place(relx=0, rely=1, x=+53, anchor=SW)
		self.curr_temp.pack() #place(relx=0.5, rely=0.5, anchor=S)
		self.curr_icon.pack() #(relx=0.5, rely=0.5, anchor=N)
		self.curr_windvane.place(relx=0.25, rely=0.165, anchor=CENTER)
		self.curr_description.pack(anchor=W)
		self.curr_wind.pack(anchor=W)
		Label(self.frame_info1, font=set_font+" 3", bg=main_bg_color).pack() # Es ist einfach nur ein Abstand
		self.curr_infolabel.pack(anchor=W)				
		self.curr_sun.pack(anchor=W)
		#self.curr_pressure.pack()
		self.curr_locname.pack(anchor=W)		
		
		#Label(self.frame_forecasts, font=(set_font, 9), fg=main_fg_color, bg=main_bg_color, text="Vorhersage").grid(row=0, column=0, columnspan=3)
		self.next1_time.grid(row=1, column=1, sticky=NW)
		self.next1_icon.grid(row=1, column=2, padx=3, pady=5)
		self.next1_temp.grid(row=1, column=3, sticky=E)
		#self.next1_description.pack()
		#self.next1_clouds.pack()
		#self.next1_wind.pack()
		self.next1_windvane.grid(row=1, column=4)
		self.next1_infolabel.grid(row=1, column=5, padx=10)
		
		self.next2_time.grid(row=2, column=1, sticky=NW)
		self.next2_icon.grid(row=2, column=2, padx=3, pady=5)
		self.next2_temp.grid(row=2, column=3, sticky=E)
		#self.next2_description.pack()
		#self.next2_clouds.pack()
		#self.next2_wind.pack()
		self.next2_windvane.grid(row=2, column=4)
		self.next2_infolabel.grid(row=2, column=5, padx=10)
		
		self.next3_time.grid(row=3, column=1, sticky=NW)
		self.next3_icon.grid(row=3, column=2, padx=3, pady=5)
		self.next3_temp.grid(row=3, column=3, sticky=E)
		#self.next3_description.pack()
		#self.next3_clouds.pack()
		#self.next3_wind.pack()
		self.next3_windvane.grid(row=3, column=4)
		self.next3_infolabel.grid(row=3, column=5, padx=10)
		
		self.button_switch_hf.place(relx=0.5, rely=0.1, anchor=NE)
		self.button_switch_hf.bind("<1>", key_control.switch_hf)
		
		self.nextday.grid(row=0, column=0, sticky=NW)
		self.nextday_icon.grid(row=0, column=1, padx=5, pady=8)
		self.nextday_temp1.grid(row=0, column=2)
		self.nextday_temp2.grid(row=0, column=3)
		
	
	def layout3(self):
		self.frame0.place_forget()
		
		# Define Frames:
		self.frame0 = Frame(window, bg=main_bg_color)
		self.frame_current = Frame(self.frame0, bg=main_bg_color) #relief? flat/sunken/raised/groove/RIDGE +borderwidth
		self.frame_info1 = Frame(self.frame0, bg=main_bg_color, borderwidth=1, relief="ridge")
		self.frame_forecasts = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="groove")
		#self.frame_next1 = Frame(self.frame0, bg="green")#, borderwidth=1, relief="ridge")
		#self.frame_next2 = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="ridge")
		#self.frame_next3 = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="ridge")
		self.frame_nextdays = Frame(self.frame0, bg=main_bg_color)
		#self.frame_nextday2 = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="ridge")
		#self.frame_nextday3 = Frame(self.frame0, bg=main_bg_color)#, borderwidth=1, relief="ridge")
		

		# Place Frames:
		self.frame0.place(relx=0.5, rely=0.5, width=440, height=255, y=-115, anchor=N)
		#self.frame_current.place(relx=0, rely=0.33, relwidth=0.25, relheight=0.33, anchor=SW)
		#self.frame_info1.place(relx=0, rely=0.33, y=+2, relwidth=0.5, relheight=0.57, anchor=NW)
		#self.frame_forecasts.place(relx=1, rely=0.05, relwidth=0.47, relheight=0.68, anchor=NE)
		#self.frame_next1.place(relx=0.25, rely=0.5, relwidth=0.25, relheight=0.5, anchor=NW)
		#self.frame_next2.place(relx=0.5, rely=0, relwidth=0.25, relheight=0.5, anchor=NW)
		#self.frame_next3.place(relx=0.75, rely=0, relwidth=0.25, relheight=0.5, anchor=NW)
		self.frame_nextdays.place(relx=0, rely=0, relwidth=1, anchor=NW) #relheight=0.262 für einen Abstand von 0.05 nach unten
		#self.frame_nextday2.place(relx=0.5, rely=0.5, relwidth=0.25, relheight=0.5, anchor=NW)
		#self.frame_nextday3.place(relx=0.75, rely=0.5, relwidth=0.25, relheight=0.5, anchor=NW)
				
		#self.disp_line = Label(self.frame0, image=self.strich, bg=main_bg_color)
		#self.disp_line.place(relx=0.53, rely=0.74, anchor=W) # rely=0.7425
		
		
		# Define Labels:
		self.import_state = Label(self.frame0, font="Arial 7", fg="red4", bg=main_bg_color)
		
		self.curr_dt = Label(self.frame0, font="Arial 7", fg="grey", bg=main_bg_color, relief="ridge", borderwidth=1) # oder groove?
		self.curr_dt_intimezone = Label(self.frame0, font="Arial 8", fg=main_fg_color, bg=main_bg_color)
		self.curr_timezone = Label(self.frame0, font="Arial 7", fg="grey", bg=main_bg_color)
		self.curr_temp = Label(self.frame_current, font=set_font+" 16", fg=main_fg_color, bg=main_bg_color)
		self.curr_icon = Label(self.frame_current, bg=main_bg_color, image=self.c_icon)
		self.curr_windvane = Label(self.frame0, bg=main_bg_color, image=self.c_windvane)
		self.curr_description = Label(self.frame_info1, font=set_font+" 11", fg=main_fg_color, bg=main_bg_color)
		self.curr_wind = Label(self.frame_info1, font=set_font+" 9", fg=main_fg_color, bg=main_bg_color)
		self.curr_sun = Label(self.frame_info1, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color)
		self.curr_locname = Label(self.frame_info1, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color)
		self.curr_infolabel = Label(self.frame_info1, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color, justify=LEFT)		
		#self.curr_pressure = Label(self.frame_current, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color, text="Luftdruck: "+"xxxx"+" hpa")
		
		
		#Labels hourly-forecasts
		self.next1_time = Label(self.frame_forecasts, font=(set_font, 8), fg=main_fg_color, bg=main_bg_color)
		self.next1_temp = Label(self.frame_forecasts, font=set_font+" 13", fg=main_fg_color, bg=main_bg_color)
		self.next1_icon = Label(self.frame_forecasts, bg=main_bg_color, image=self.n1_icon)
		#self.next1_description = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next1_clouds = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next1_wind = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		self.next1_windvane = Label(self.frame_forecasts, bg=main_bg_color, image=self.n1_windvane)
		self.next1_infolabel = Label(self.frame_forecasts, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		
		self.next2_time = Label(self.frame_forecasts, font=(set_font, 8), fg=main_fg_color, bg=main_bg_color)
		self.next2_temp = Label(self.frame_forecasts, font=set_font+" 13", fg=main_fg_color, bg=main_bg_color)
		self.next2_icon = Label(self.frame_forecasts, bg=main_bg_color, image=self.n2_icon)
		#self.next2_description = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next2_clouds = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next2_wind = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		self.next2_windvane = Label(self.frame_forecasts, bg=main_bg_color, image=self.n2_windvane)
		self.next2_infolabel = Label(self.frame_forecasts, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)

		self.next3_time = Label(self.frame_forecasts, font=(set_font, 8), fg=main_fg_color, bg=main_bg_color)
		self.next3_temp = Label(self.frame_forecasts, font=set_font+" 13", fg=main_fg_color, bg=main_bg_color)
		self.next3_icon = Label(self.frame_forecasts, bg=main_bg_color, image=self.n3_icon)
		#self.next3_description = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next3_clouds = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		#self.next3_wind = Label(self.frame_next1, font=set_font+" 10", fg=main_fg_color, bg=main_bg_color)
		self.next3_windvane = Label(self.frame_forecasts, bg=main_bg_color, image=self.n3_windvane)
		self.next3_infolabel = Label(self.frame_forecasts, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		
		
		#Labels Nextday
		self.nextday = Label(self.frame_nextdays, font=(set_font, 8, "bold"), fg=main_fg_color, bg=main_bg_color)
		self.nextday_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_noon_icon)
		self.nextday_temp1 = Label(self.frame_nextdays, font=set_font+" 12", fg=main_fg_color, bg=main_bg_color)
		self.nextday_temp2 = Label(self.frame_nextdays, font=set_font+" 12", fg="grey", bg=main_bg_color)
		
		# Labels Nextday with daytime
		self.nextday1 = Label(self.frame_nextdays, font=(set_font, 9), fg=main_fg_color, bg=main_bg_color)
		self.nextday1_temp1 = Label(self.frame_nextdays, font=set_font+" 12", fg=main_fg_color, bg=main_bg_color)
		self.nextday1_temp2 = Label(self.frame_nextdays, font=set_font+" 12", fg="grey", bg=main_bg_color)
		self.nextday1_night_temp = Label(self.frame_nextdays, font=(set_font, 11), fg=main_fg_color, bg=main_bg_color)
		self.nextday1_night_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_night_icon)
		self.nextday1_night_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_night_windvane)
		self.nextday1_night_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday1_morning_temp = Label(self.frame_nextdays, font=(set_font, 11), fg=main_fg_color, bg=main_bg_color)
		self.nextday1_morning_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_morning_icon)
		self.nextday1_morning_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_morning_windvane)
		self.nextday1_morning_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday1_noon_temp = Label(self.frame_nextdays, font=(set_font, 11), fg=main_fg_color, bg=main_bg_color)
		self.nextday1_noon_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_noon_icon)
		self.nextday1_noon_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_noon_windvane)
		self.nextday1_noon_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday1_evening_temp = Label(self.frame_nextdays, font=(set_font, 11), fg=main_fg_color, bg=main_bg_color)
		self.nextday1_evening_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_evening_icon)
		self.nextday1_evening_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday1_evening_windvane)
		self.nextday1_evening_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		
		self.nextday2 = Label(self.frame_nextdays, font=(set_font, 9), fg=main_fg_color, bg=main_bg_color)
		self.nextday2_temp1 = Label(self.frame_nextdays, font=set_font+" 12", fg=main_fg_color, bg=main_bg_color)
		self.nextday2_temp2 = Label(self.frame_nextdays, font=set_font+" 12", fg="grey", bg=main_bg_color)
		self.nextday2_night_temp = Label(self.frame_nextdays, font=(set_font, 11), fg=main_fg_color, bg=main_bg_color)
		self.nextday2_night_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday2_night_icon)
		self.nextday2_night_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday2_night_windvane)
		self.nextday2_night_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday2_morning_temp = Label(self.frame_nextdays, font=(set_font, 11), fg=main_fg_color, bg=main_bg_color)
		self.nextday2_morning_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday2_morning_icon)
		self.nextday2_morning_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday2_morning_windvane)
		self.nextday2_morning_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday2_noon_temp = Label(self.frame_nextdays, font=(set_font, 11), fg=main_fg_color, bg=main_bg_color)
		self.nextday2_noon_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday2_noon_icon)
		self.nextday2_noon_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday2_noon_windvane)
		self.nextday2_noon_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday2_evening_temp = Label(self.frame_nextdays, font=(set_font, 11), fg=main_fg_color, bg=main_bg_color)
		self.nextday2_evening_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday2_evening_icon)
		self.nextday2_evening_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday2_evening_windvane)
		self.nextday2_evening_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)	
		
		self.nextday3 = Label(self.frame_nextdays, font=(set_font, 9), fg=main_fg_color, bg=main_bg_color)
		self.nextday3_temp1 = Label(self.frame_nextdays, font=set_font+" 12", fg=main_fg_color, bg=main_bg_color)
		self.nextday3_temp2 = Label(self.frame_nextdays, font=set_font+" 12", fg="grey", bg=main_bg_color)
		self.nextday3_night_temp = Label(self.frame_nextdays, font=(set_font, 10), fg=main_fg_color, bg=main_bg_color)
		self.nextday3_night_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday3_night_icon)
		self.nextday3_night_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday3_night_windvane)
		self.nextday3_night_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday3_morning_temp = Label(self.frame_nextdays, font=(set_font, 10), fg=main_fg_color, bg=main_bg_color)
		self.nextday3_morning_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday3_morning_icon)
		self.nextday3_morning_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday3_morning_windvane)
		self.nextday3_morning_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday3_noon_temp = Label(self.frame_nextdays, font=(set_font, 10), fg=main_fg_color, bg=main_bg_color)
		self.nextday3_noon_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday3_noon_icon)
		self.nextday3_noon_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday3_noon_windvane)
		self.nextday3_noon_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		self.nextday3_evening_temp = Label(self.frame_nextdays, font=(set_font, 10), fg=main_fg_color, bg=main_bg_color)
		self.nextday3_evening_icon = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday3_evening_icon)
		self.nextday3_evening_windvane = Label(self.frame_nextdays, bg=main_bg_color, image=self.nday3_evening_windvane)
		self.nextday3_evening_infolabel = Label(self.frame_nextdays, font=set_font+" 7", fg=main_fg_color, bg=main_bg_color, justify=CENTER)
		
		self.button_switch_hf = Label(self.frame0)
		
		
		self.update_widgets()
		
		
		# Labels packen
		""" Uhrzeit und Zeitzone sind in dieser Ansicht nicht so wichtig
		
		self.import_state.place(relx=0.5, rely=1, x=-30, anchor=SE)
		self.curr_dt.place(relx=0.5, rely=1, anchor=SE)
		self.curr_dt_intimezone.place(relx=0, rely=1, anchor=SW)
		self.curr_timezone.place(relx=0, rely=1, x=+53, anchor=SW)
		
		"""
		#self.curr_temp.pack() #place(relx=0.5, rely=0.5, anchor=S)
		#self.curr_icon.pack() #(relx=0.5, rely=0.5, anchor=N)
		#self.curr_windvane.place(relx=0.25, rely=0.165, anchor=CENTER)
		#self.curr_description.pack(anchor=W)
		#self.curr_wind.pack(anchor=W)
		#Label(self.frame_info1, font=set_font+" 3", bg=main_bg_color).pack() # Es ist einfach nur ein Abstand
		#self.curr_infolabel.pack(anchor=W)				
		#self.curr_sun.pack(anchor=W)
		#self.curr_pressure.pack()
		#self.curr_locname.pack(anchor=W)		
		
		#Label(self.frame_forecasts, font=(set_font, 9), fg=main_fg_color, bg=main_bg_color, text="Vorhersage").grid(row=0, column=0, columnspan=3)
		#self.next1_time.grid(row=1, column=1, sticky=NW)
		#self.next1_icon.grid(row=1, column=2, padx=3, pady=5)
		#self.next1_temp.grid(row=1, column=3, sticky=E)
		#self.next1_description.pack()
		#self.next1_clouds.pack()
		#self.next1_wind.pack()
		#self.next1_windvane.grid(row=1, column=4)
		#self.next1_infolabel.grid(row=1, column=5, padx=10)
		
		#self.next2_time.grid(row=2, column=1, sticky=NW)
		#self.next2_icon.grid(row=2, column=2, padx=3, pady=5)
		#self.next2_temp.grid(row=2, column=3, sticky=E)
		#self.next2_description.pack()
		#self.next2_clouds.pack()
		#self.next2_wind.pack()
		#self.next2_windvane.grid(row=2, column=4)
		#self.next2_infolabel.grid(row=2, column=5, padx=10)
		
		#self.next3_time.grid(row=3, column=1, sticky=NW)
		#self.next3_icon.grid(row=3, column=2, padx=3, pady=5)
		#self.next3_temp.grid(row=3, column=3, sticky=E)
		#self.next3_description.pack()
		#self.next3_clouds.pack()
		#self.next3_wind.pack()
		#self.next3_windvane.grid(row=3, column=4)
		#self.next3_infolabel.grid(row=3, column=5, padx=10)
		
		
		#self.nextday.grid(row=0, column=0, sticky=NW)
		#self.nextday_icon.grid(row=0, column=1, padx=5, pady=8)
		#self.nextday_temp1.grid(row=0, column=2)
		#self.nextday_temp2.grid(row=0, column=3)
		
		Label(self.frame_nextdays, font=(set_font, 10, "bold"), fg=main_fg_color, bg=main_bg_color, text=lang[my_language]["night"]).grid(row=0, column=1, columnspan=2)
		Label(self.frame_nextdays, font=(set_font, 10, "bold"), fg=main_fg_color, bg=main_bg_color, text=lang[my_language]["morning"]).grid(row=0, column=3, columnspan=2)
		Label(self.frame_nextdays, font=(set_font, 10, "bold"), fg=main_fg_color, bg=main_bg_color, text=lang[my_language]["noon"]).grid(row=0, column=5, columnspan=2)
		Label(self.frame_nextdays, font=(set_font, 10, "bold"), fg=main_fg_color, bg=main_bg_color, text=lang[my_language]["evening"]).grid(row=0, column=7, columnspan=2)
		Label(self.frame_nextdays, font=(set_font, 3), bg=main_bg_color).grid(row=1, column=2) # Abstand (Zeile)
		Label(self.frame_nextdays, font=(set_font, 10), bg=main_bg_color).grid(row=0, column=9) # Abstand (Spalte)
		
		self.nextday1.grid(row=2, column=0, sticky=NW)
		self.nextday1_night_icon.grid(row=2, column=1, columnspan=2, padx=12)
		self.nextday1_night_temp.grid(row=3, column=1, sticky=E)
		self.nextday1_night_windvane.grid(row=3, column=2, sticky=W)
		#self.nextday1_night_infolabel.grid()
		self.nextday1_morning_icon.grid(row=2, column=3, columnspan=2, padx=12)
		self.nextday1_morning_temp.grid(row=3, column=3, sticky=E)
		self.nextday1_morning_windvane.grid(row=3, column=4, sticky=W)
		#self.nextday1_morning_infolabel.grid()	
		self.nextday1_noon_icon.grid(row=2, column=5, columnspan=2, padx=12)
		self.nextday1_noon_temp.grid(row=3, column=5, sticky=E)
		self.nextday1_noon_windvane.grid(row=3, column=6, sticky=W)
		#self.nextday1_noon_infolabel.grid()	
		self.nextday1_evening_icon.grid(row=2, column=7, columnspan=2, padx=12)
		self.nextday1_evening_temp.grid(row=3, column=7, sticky=E)
		self.nextday1_evening_windvane.grid(row=3, column=8, sticky=W)
		#self.nextday1_evening_infolabel.grid()
		Label(self.frame_nextdays, font=(set_font, 10), bg=main_bg_color, text=" ").grid(row=2, column=9) # Abstand (Spalte)
		self.nextday1_temp1.grid(row=2, column=10, sticky=E)
		self.nextday1_temp2.grid(row=2, column=11, sticky=W)
		
		Label(self.frame_nextdays, font=(set_font, 3), bg=main_bg_color).grid(row=4, column=2) # Abstand (Zeile)
		
		
		self.nextday2.grid(row=5, column=0, sticky=NW)
		self.nextday2_night_icon.grid(row=5, column=1, columnspan=2, padx=12)
		self.nextday2_night_temp.grid(row=6, column=1, sticky=E)
		self.nextday2_night_windvane.grid(row=6, column=2, sticky=W)
		#self.nextday2_night_infolabel.grid()
		self.nextday2_morning_icon.grid(row=5, column=3, columnspan=2, padx=12)
		self.nextday2_morning_temp.grid(row=6, column=3, sticky=E)
		self.nextday2_morning_windvane.grid(row=6, column=4, sticky=W)
		#self.nextday2_morning_infolabel.grid()	
		self.nextday2_noon_icon.grid(row=5, column=5, columnspan=2, padx=12)
		self.nextday2_noon_temp.grid(row=6, column=5, sticky=E)
		self.nextday2_noon_windvane.grid(row=6, column=6, sticky=W)
		#self.nextday2_noon_infolabel.grid()	
		self.nextday2_evening_icon.grid(row=5, column=7, columnspan=2, padx=12)
		self.nextday2_evening_temp.grid(row=6, column=7, sticky=E)
		self.nextday2_evening_windvane.grid(row=6, column=8, sticky=W)
		#self.nextday2_evening_infolabel.grid()
		self.nextday2_temp1.grid(row=5, column=10, sticky=E)
		self.nextday2_temp2.grid(row=5, column=11, sticky=W)
		
		Label(self.frame_nextdays, font=(set_font, 3), bg=main_bg_color).grid(row=7, column=2) # Abstand (Zeile)
		
		
		self.nextday3.grid(row=8, column=0, sticky=NW)
		self.nextday3_night_icon.grid(row=8, column=1, columnspan=2, padx=12)
		self.nextday3_night_temp.grid(row=9, column=1, sticky=E)
		self.nextday3_night_windvane.grid(row=9, column=2, sticky=W)
		#self.nextday3_night_infolabel.grid()
		self.nextday3_morning_icon.grid(row=8, column=3, columnspan=2, padx=12)
		self.nextday3_morning_temp.grid(row=9, column=3, sticky=E)
		self.nextday3_morning_windvane.grid(row=9, column=4, sticky=W)
		#self.nextday3_morning_infolabel.grid()	
		self.nextday3_noon_icon.grid(row=8, column=5, columnspan=2, padx=12)
		self.nextday3_noon_temp.grid(row=9, column=5, sticky=E)
		self.nextday3_noon_windvane.grid(row=9, column=6, sticky=W)
		#self.nextday3_noon_infolabel.grid()	
		self.nextday3_evening_icon.grid(row=8, column=7, columnspan=2, padx=12)
		self.nextday3_evening_temp.grid(row=9, column=7, sticky=E)
		self.nextday3_evening_windvane.grid(row=9, column=8, sticky=W)
		#self.nextday3_evening_infolabel.grid()
		self.nextday3_temp1.grid(row=8, column=10, sticky=E)
		self.nextday3_temp2.grid(row=8, column=11, sticky=W)
				

	def update_data(self):
		
		def import_current():
			# Import all values of current weather:
			self.c_locname = self.current_data.get("name")
			self.c_cityid = self.current_data.get("id")
			
			# Get timezone and locale times of weather location via coordinates:
			if "coord" in self.current_data:
				self.c_lon = self.current_data["coord"].get("lon")
				self.c_lat = self.current_data["coord"].get("lat")
				try:
					self.tz = timezone(TimezoneFinder().timezone_at(lng=self.c_lon, lat=self.c_lat))
					self.c_dt_intimezone = datetime.fromtimestamp(self.current_data.get("dt"), tz=self.tz)
					# Die längere und umständlichere Methode wäre:
					#self.c_dt_intimezone = datetime.utcfromtimestamp(self.current_data.get("dt")).replace(tzinfo=utc).astimezone(self.tz)
					
					self.c_timezone = self.c_dt_intimezone.strftime("UTC%z")
					# Vielleicht hier besser über timezone.fromutc(aware datetime instance) oder timezone.tzname(aware datetime instance)
					# oder tzinfo.utcoffset(aware datetime instance)
					# Setzt import von datetime.timezone bzw. datetime.tzinfo voraus.
					self.c_zone_timezone = self.tz.zone
					
				except:
					self.tz = None
					self.c_timezone = "tz n. a."
								
			else:
				self.tz = None
				self.c_timezone = "tz n. a."
								
			if "main" in self.current_data:
				if "temp" in self.current_data["main"]:
					self.c_temp = round(self.current_data["main"].get("temp"))
				self.c_humidity = self.current_data["main"].get("humidity")
				self.c_pressure = self.current_data["main"].get("pressure")
			if "weather" in self.current_data:
				self.c_iconid = self.current_data["weather"][0].get("icon")
				self.c_description = self.current_data["weather"][0].get("description")
			self.c_icon = PhotoImage(file=img_dir + self.c_iconid + ".png")
			if "wind" in self.current_data:
				self.c_windspeed = (self.current_data["wind"].get("speed"))
				self.c_winddeg = self.current_data["wind"].get("deg")
			if "sys" in self.current_data:
				self.c_country = self.current_data["sys"].get("country")
				try:
					self.c_sunrise = datetime.fromtimestamp(self.current_data["sys"]["sunrise"], tz=self.tz).strftime("%H:%M")
					self.c_sunset = datetime.fromtimestamp(self.current_data["sys"]["sunset"], tz=self.tz).strftime("%H:%M")
					# Andere Methode (länger):
					#self.c_sunrise = datetime.utcfromtimestamp(self.current_data["sys"]["sunrise"]).replace(tzinfo=utc).astimezone(self.tz)
					#self.c_sunset = datetime.utcfromtimestamp(self.current_data["sys"]["sunset"]).replace(tzinfo=utc).astimezone(self.tz)
				except:
					pass
			if "clouds" in self.current_data:
				self.c_clouds = self.current_data["clouds"].get("all")
			if "rain" in self.current_data:
				self.c_rain = self.current_data["rain"].get("3h")
			if "visibility" in self.current_data:
				self.c_visibility = round(self.current_data.get("visibility") / 1000, 1)
						
		def import_forecast():
			# Import all values of weather forecast (next hours):
			if "list" in self.forecast_data:
				
				
				# forecast 6 hours:
				
				#self.n1_b_time = datetime.utcfromtimestamp(self.forecast_data["list"][1].get("dt")).replace(tzinfo=utc).astimezone(self.tz).hour
				self.n1_b_time = datetime.fromtimestamp(self.forecast_data["list"][1].get("dt"), tz=self.tz).hour
				if "main" in self.forecast_data["list"][1] and "temp" in self.forecast_data["list"][1]["main"]:
					self.n1_b_temp = round(self.forecast_data["list"][1]["main"]["temp"])
				if "weather" in self.forecast_data["list"][1]:
					self.n1_b_iconid = self.forecast_data["list"][1]["weather"][0].get("icon")
					self.n1_b_description = self.forecast_data["list"][1]["weather"][0].get("description")
				if "clouds" in self.forecast_data["list"][1]:
					self.n1_b_clouds = self.forecast_data["list"][1]["clouds"].get("all")
				if "wind" in self.forecast_data["list"][1]:
					self.n1_b_winddeg = self.forecast_data["list"][1]["wind"].get("deg")
					if "speed" in self.forecast_data["list"][1]["wind"]:
						self.n1_b_windspeed = self.forecast_data["list"][1]["wind"]["speed"]
						self.n1_b_windspeed = round(self.n1_b_windspeed, 1)				
				
				#self.n2_b_time = datetime.utcfromtimestamp(self.forecast_data["list"][3].get("dt")).replace(tzinfo=utc).astimezone(self.tz).hour
				self.n2_b_time = datetime.fromtimestamp(self.forecast_data["list"][3].get("dt"), tz=self.tz).hour
				if "main" in self.forecast_data["list"][3] and "temp" in self.forecast_data["list"][3]["main"]:
					self.n2_b_temp = round(self.forecast_data["list"][3]["main"]["temp"])
				if "weather" in self.forecast_data["list"][3]:
					self.n2_b_iconid = self.forecast_data["list"][3]["weather"][0].get("icon")
					self.n2_b_description = self.forecast_data["list"][3]["weather"][0].get("description")
				if "clouds" in self.forecast_data["list"][3]:
					self.n2_b_clouds = self.forecast_data["list"][3]["clouds"].get("all")
				if "wind" in self.forecast_data["list"][3]:
					self.n2_b_winddeg = self.forecast_data["list"][3]["wind"].get("deg")
					if "speed" in self.forecast_data["list"][3]["wind"]:
						self.n2_b_windspeed = self.forecast_data["list"][3]["wind"]["speed"]
						self.n2_b_windspeed = round(self.n2_b_windspeed, 1)
					
				#self.n3_b_time = datetime.utcfromtimestamp(self.forecast_data["list"][5].get("dt")).replace(tzinfo=utc).astimezone(self.tz).hour
				self.n3_b_time = datetime.fromtimestamp(self.forecast_data["list"][5].get("dt"), tz=self.tz).hour
				self.n3_b_day = datetime.fromtimestamp(self.forecast_data["list"][5].get("dt"), tz=self.tz).day
				if "main" in self.forecast_data["list"][5] and "temp" in self.forecast_data["list"][5]["main"]:
					self.n3_b_temp = round(self.forecast_data["list"][5]["main"]["temp"])
				if "weather" in self.forecast_data["list"][5]:
					self.n3_b_iconid = self.forecast_data["list"][5]["weather"][0].get("icon")
					self.n3_b_description = self.forecast_data["list"][5]["weather"][0].get("description")
				if "clouds" in self.forecast_data["list"][5]:
					self.n3_b_clouds = self.forecast_data["list"][5]["clouds"].get("all")
				if "wind" in self.forecast_data["list"][5]:
					self.n3_b_winddeg = self.forecast_data["list"][5]["wind"].get("deg")
					if "speed" in self.forecast_data["list"][5]["wind"]:
						self.n3_b_windspeed = self.forecast_data["list"][5]["wind"]["speed"]
						self.n3_b_windspeed = round(self.n3_b_windspeed, 1)
				
				
				# forecast 3 hours:
				
				#self.n1_a_time = datetime.utcfromtimestamp(self.forecast_data["list"][1].get("dt")).replace(tzinfo=utc).astimezone(self.tz).hour
				self.n1_a_time = datetime.fromtimestamp(self.forecast_data["list"][0].get("dt"), tz=self.tz).hour
				if "main" in self.forecast_data["list"][0] and "temp" in self.forecast_data["list"][0]["main"]:
					self.n1_a_temp = round(self.forecast_data["list"][0]["main"]["temp"])
				if "weather" in self.forecast_data["list"][0]:
					self.n1_a_iconid = self.forecast_data["list"][0]["weather"][0].get("icon")
					self.n1_a_description = self.forecast_data["list"][0]["weather"][0].get("description")
				if "clouds" in self.forecast_data["list"][0]:
					self.n1_a_clouds = self.forecast_data["list"][0]["clouds"].get("all")
				if "wind" in self.forecast_data["list"][0]:
					self.n1_a_winddeg = self.forecast_data["list"][0]["wind"].get("deg")
					if "speed" in self.forecast_data["list"][0]["wind"]:
						self.n1_a_windspeed = self.forecast_data["list"][0]["wind"]["speed"]
						self.n1_a_windspeed = round(self.n1_a_windspeed, 1)				
				
				#self.n2_a_time = datetime.utcfromtimestamp(self.forecast_data["list"][3].get("dt")).replace(tzinfo=utc).astimezone(self.tz).hour
				self.n2_a_time = datetime.fromtimestamp(self.forecast_data["list"][1].get("dt"), tz=self.tz).hour
				if "main" in self.forecast_data["list"][1] and "temp" in self.forecast_data["list"][1]["main"]:
					self.n2_a_temp = round(self.forecast_data["list"][1]["main"]["temp"])
				if "weather" in self.forecast_data["list"][1]:
					self.n2_a_iconid = self.forecast_data["list"][1]["weather"][0].get("icon")
					self.n2_a_description = self.forecast_data["list"][1]["weather"][0].get("description")
				if "clouds" in self.forecast_data["list"][1]:
					self.n2_a_clouds = self.forecast_data["list"][1]["clouds"].get("all")
				if "wind" in self.forecast_data["list"][1]:
					self.n2_a_winddeg = self.forecast_data["list"][1]["wind"].get("deg")
					if "speed" in self.forecast_data["list"][1]["wind"]:
						self.n2_a_windspeed = self.forecast_data["list"][1]["wind"]["speed"]
						self.n2_a_windspeed = round(self.n2_a_windspeed, 1)
				
				#self.n3_a_time = datetime.utcfromtimestamp(self.forecast_data["list"][5].get("dt")).replace(tzinfo=utc).astimezone(self.tz).hour
				self.n3_a_time = datetime.fromtimestamp(self.forecast_data["list"][2].get("dt"), tz=self.tz).hour
				self.n3_a_day = datetime.fromtimestamp(self.forecast_data["list"][2].get("dt"), tz=self.tz).day
				if "main" in self.forecast_data["list"][2] and "temp" in self.forecast_data["list"][2]["main"]:
					self.n3_a_temp = round(self.forecast_data["list"][2]["main"]["temp"])
				if "weather" in self.forecast_data["list"][2]:
					self.n3_a_iconid = self.forecast_data["list"][2]["weather"][0].get("icon")
					self.n3_a_description = self.forecast_data["list"][2]["weather"][0].get("description")
				if "clouds" in self.forecast_data["list"][2]:
					self.n3_a_clouds = self.forecast_data["list"][2]["clouds"].get("all")
				if "wind" in self.forecast_data["list"][2]:
					self.n3_a_winddeg = self.forecast_data["list"][2]["wind"].get("deg")
					if "speed" in self.forecast_data["list"][2]["wind"]:
						self.n3_a_windspeed = self.forecast_data["list"][2]["wind"]["speed"]
						self.n3_a_windspeed = round(self.n3_a_windspeed, 1)
				
		def import_nextdays():
			cday_temp_list = []
			nday1_temp_list = []
			nday2_temp_list = []
			nday3_temp_list = []
			
			if "list" in self.forecast_data and "dt" in self.current_data:
				current_date = datetime.fromtimestamp(self.current_data["dt"],tz=self.tz)
				
				for d in self.forecast_data["list"]:
					check_date = 0 			# Otherwise error in next row if d.get("dt") doesn't exist or is None.
					check_date = datetime.fromtimestamp(d.get("dt"),tz=self.tz) 
					day_timedelta = (check_date.replace(hour=0, minute=0, second=0) - current_date.replace(hour=0, minute=0, second=0)).days
					
					if day_timedelta == 0 and "main" in d:
						cday_temp_list.append(d["main"].get("temp"))
					
					if day_timedelta == 1:
						self.nday1 = lang[my_language]["tomorrow"]
						# get Min/Max temp of the day by adding all temps from day to a list:
						if "main" in d:
							nday1_temp_list.append(d["main"].get("temp"))
						
						# self.nday1 data:						
						if 1 <= check_date.hour <= 3: # Nachts
							if "weather" in d:
								self.nday1_night_iconid = d["weather"][0].get("icon")
								#self.nday1_night_icon = PhotoImage(file=img_dir + self.nday1_night_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday1_night_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday1_night_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday1_night_windspeed = d["wind"]["speed"]
									self.nday1_night_windspeed = round(self.nday1_night_windspeed, 1)
						if 7 <= check_date.hour <= 9: # Morgens
							if "weather" in d:
								self.nday1_morning_iconid = d["weather"][0].get("icon")
								#self.nday1_morning_icon = PhotoImage(file=img_dir + self.nday1_morning_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday1_morning_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday1_morning_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday1_morning_windspeed = d["wind"]["speed"]
									self.nday1_morning_windspeed = round(self.nday1_morning_windspeed, 1)
						if 13 <= check_date.hour <= 15: # Mittags
							if "weather" in d:
								self.nday1_noon_iconid = d["weather"][0].get("icon")
								#self.nday1_noon_icon = PhotoImage(file=img_dir + self.nday1_noon_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday1_noon_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday1_noon_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday1_noon_windspeed = d["wind"]["speed"]
									self.nday1_noon_windspeed = round(self.nday1_noon_windspeed, 1)
						if 19 <= check_date.hour <= 21: # Mittags
							if "weather" in d:
								self.nday1_evening_iconid = d["weather"][0].get("icon")
								#self.nday1_evening_icon = PhotoImage(file=img_dir + self.nday1_evening_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday1_evening_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday1_evening_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday1_evening_windspeed = d["wind"]["speed"]
									self.nday1_evening_windspeed = round(self.nday1_evening_windspeed, 1)
				
					if day_timedelta == 2:
						self.nday2 = check_date.isoweekday()
						# get Min/Max temp of the day by adding all temps from day to a list:
						if "main" in d:
							nday2_temp_list.append(d["main"].get("temp"))
						
						# self.nday1 data:						
						if 1 <= check_date.hour <= 3: # Nachts
							if "weather" in d:
								self.nday2_night_iconid = d["weather"][0].get("icon")
								#self.nday2_night_icon = PhotoImage(file=img_dir + self.nday2_night_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday2_night_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday2_night_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday2_night_windspeed = d["wind"]["speed"]
									self.nday2_night_windspeed = round(self.nday2_night_windspeed, 1)
						if 7 <= check_date.hour <= 9: # Morgens
							if "weather" in d:
								self.nday2_morning_iconid = d["weather"][0].get("icon")
								#self.nday2_morning_icon = PhotoImage(file=img_dir + self.nday2_morning_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday2_morning_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday2_morning_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday2_morning_windspeed = d["wind"]["speed"]
									self.nday2_morning_windspeed = round(self.nday2_morning_windspeed, 1)
						if 13 <= check_date.hour <= 15: # Mittags
							if "weather" in d:
								self.nday2_noon_iconid = d["weather"][0].get("icon")
								#self.nday2_noon_icon = PhotoImage(file=img_dir + self.nday2_noon_iconid + ".png")

							if "main" in d and "temp" in d["main"]:
								self.nday2_noon_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday2_noon_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday2_noon_windspeed = d["wind"]["speed"]
									self.nday2_noon_windspeed = round(self.nday2_noon_windspeed, 1)
						if 19 <= check_date.hour <= 21: # Mittags
							if "weather" in d:
								self.nday2_evening_iconid = d["weather"][0].get("icon")
								#self.nday2_evening_icon = PhotoImage(file=img_dir + self.nday2_evening_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday2_evening_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday2_evening_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday2_evening_windspeed = d["wind"]["speed"]
									self.nday2_evening_windspeed = round(self.nday2_evening_windspeed, 1)
					
					if day_timedelta == 3:
						self.nday3 = check_date.isoweekday()
						# get Min/Max temp of the day by adding all temps from day to a list:
						if "main" in d:
							nday3_temp_list.append(d["main"].get("temp"))
						
						# self.nday1 data:						
						if 1 <= check_date.hour <= 3: # Nachts
							if "weather" in d:
								self.nday3_night_iconid = d["weather"][0].get("icon")
								#self.nday3_night_icon = PhotoImage(file=img_dir + self.nday3_night_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday3_night_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday3_night_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday3_night_windspeed = d["wind"]["speed"]
									self.nday3_night_windspeed = round(self.nday3_night_windspeed, 1)
						if 7 <= check_date.hour <= 9: # Morgens
							if "weather" in d:
								self.nday3_morning_iconid = d["weather"][0].get("icon")
								#self.nday3_morning_icon = PhotoImage(file=img_dir + self.nday3_morning_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday3_morning_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday3_morning_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday3_morning_windspeed = d["wind"]["speed"]
									self.nday3_morning_windspeed = round(self.nday3_morning_windspeed, 1)
						if 13 <= check_date.hour <= 15: # Mittags
							if "weather" in d:
								self.nday3_noon_iconid = d["weather"][0].get("icon")
								#self.nday3_noon_icon = PhotoImage(file=img_dir + self.nday3_noon_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday3_noon_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday3_noon_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday3_noon_windspeed = d["wind"]["speed"]
									self.nday3_noon_windspeed = round(self.nday3_noon_windspeed, 1)
						if 19 <= check_date.hour <= 21: # Mittags
							if "weather" in d:
								self.nday3_evening_iconid = d["weather"][0].get("icon")
								#self.nday3_evening_icon = PhotoImage(file=img_dir + self.nday3_evening_iconid + ".png")
							if "main" in d and "temp" in d["main"]:
								self.nday3_evening_temp = round(d["main"]["temp"])
							if "wind" in d:
								self.nday3_evening_winddeg = d["wind"].get("deg")
								if "speed" in d["wind"]:
									self.nday3_evening_windspeed = d["wind"]["speed"]
									self.nday3_evening_windspeed = round(self.nday3_evening_windspeed, 1)
				
				try:
					self.c_temp_min = round(min(cday_temp_list)) # If list is empty it will raise a ValueError
					self.c_temp_max = round(max(cday_temp_list)) # If list is empty it will raise a ValueError
				except:
					self.c_temp_min = self.c_temp
					self.c_temp_max = self.c_temp
				self.nday1_temp_min = round(min(nday1_temp_list)) # If list is empty it will raise a ValueError
				self.nday1_temp_max = round(max(nday1_temp_list)) # If list is empty it will raise a ValueError
				self.nday2_temp_min = round(min(nday2_temp_list)) # If list is empty it will raise a ValueError
				self.nday2_temp_max = round(max(nday2_temp_list)) # If list is empty it will raise a ValueError
				self.nday3_temp_min = round(min(nday3_temp_list)) # If list is empty it will raise a ValueError
				self.nday3_temp_max = round(max(nday3_temp_list)) # If list is empty it will raise a ValueError
		
		
		self.current_data = current_data
		self.forecast_data = forecast_data
		self.c_dt = c_dt
		
		
		import_current()
		import_forecast()
		import_nextdays()
		self.update_widgets()


	def update_widgets(self):
		
		def convert_winddeg(deg):
			if type(deg) != float and type(deg) != int:
				return "-"
			# or:
			#if deg == None or type(deg) == str:
			#	return "-"
			else:
				if deg >= 337.5 or deg < 22.5:
					return "N"
				elif 22.5 < deg < 67.5:
					return "NE"
				elif 67.5 <= deg <= 112.5:
					return "E"
				elif 112.5 < deg < 157.5:
					return "SE"
				elif 157.5 <= deg <= 202.5:
					return "S"
				elif 202.5 < deg < 247.5:
					return "SW"
				elif 247.5 <= deg <= 292.5:
					return "W"
				elif 292.5 < deg < 337.5:
					return "NW"

		def convert_windspeed(speed):
			if type(speed) != float and type(speed) != int:
				return "--"
			#or:
			#if speed == None or type(speed) == str:
			#	return "-- Wind"
			else:
				if unit_speed == " mph":
					speed *= 0.44704
				speed = float(speed)
				if speed < 0.3:
					return "0Bft"
				elif speed >= 0.3 and speed < 1.6:
					return "1Bft"
				elif speed  >= 1.6 and speed < 3.4:
					return "2Bft"
				elif speed  >= 3.4 and speed < 5.5:
					return "3Bft"
				elif speed  >= 5.5 and speed < 8.0:
					return "4Bft"
				elif speed  >= 8.0 and speed < 10.8:
					return "5Bft"
				elif speed  >= 10.8 and speed < 13.9:
					return "6Bft"
				elif speed  >= 13.9 and speed < 17.2:
					return "7Bft"
				elif speed  >= 17.2 and speed < 20.8:
					return "8Bft"
				elif speed  >= 20.8 and speed < 24.5:
					return "9Bft"
				elif speed  >= 24.5 and speed < 28.5:
					return "10Bft"
				elif speed  >= 28.5 and speed < 32.7:
					return "11Bft"
				elif speed  >= 32.7:
					return "12Bft"
			"""				
			=========================
			Windgeschwindigkeiten:
			nach https://de.wikipedia.org/wiki/Beaufortskala
			und Benennungen nach https://de.wikipedia.org/wiki/Windgeschwindigkeit
							bzw. http://www.wettergefahren.de/warnungen/windwarnskala.html des DWD

			m/s
			0,0 – <0,3   | Windstill
			0,3 – <1,6   | geringer Wind / leiser Zug
			1,6 – <3,4   | leichter Wind / leichte Brise
			3,4 – <5,5   | schwacher Wind / schwache Brise
			5,5 – <8,0   | mäßiger Wind / mäßige Brise
			8,0 – <10,8  | frischer Wind / frische Brise
			10,8 – <13,9 | starker Wind
			13,9 – <17,2 | stark bis stürmischer Wind / steifer Wind
			17,2 – <20,8 | stürmischer Wind
			20,8 – <24,5 | Sturm
			24,5 – <28,5 | schwerer Sturm
			28,5 – <32,7 | orkanartiger Sturm
			≥ 32,7       | Orkan
			========================
		"""
		
		def windvane(speed, degree):
			if unit_speed == " mph":
					try:					# speed could not only be an int or a float but also None or a string -> Maybe TypeError
						speed *= 0.44704
					except:
						pass

			if degree == None:
				if type(speed) != float and type(speed) != int:
					return "noinfo", 0
				elif round(speed * 1.94384) < 1:
					return "0kn", 0
				else:
					return "noinfo", 0
			elif type(speed) != float and type(speed) != int:
				return "noinfo", 0
			else:
				kn = round(speed * 1.94384)
				rotate = -degree
				if kn < 1:
					return "0kn", 0
				elif 1 <= kn <= 5:
					return "5kn", rotate
				elif 5 < kn <= 10:
					return "10kn", rotate
				elif 10 < kn <= 15:
					return "15kn", rotate
				elif 15 < kn <= 20:
					return "20kn", rotate
				elif 20 < kn <= 25:
					return "25kn", rotate
				elif 25 < kn <= 30:
					return "30kn", rotate
				elif 30 < kn <= 35:
					return "35kn", rotate
				elif 35 < kn <= 40:
					return "40kn", rotate
				elif 40 < kn <= 45:
					return "45kn", rotate
				elif 45 < kn <= 50:
					return "50kn", rotate
				elif 50 < kn <= 55:
					return "55kn", rotate
				elif 55 < kn <= 63:
					return "60kn", rotate
				elif 63 < kn <= 100:
					return "100kn", rotate
				elif kn > 100:
					return "105kn", rotate
			
		
		# Update Labels:
		
		def update_widgets_current():
					
			if offline_state:
				self.import_state.config(fg="red4", text="offline")
			elif no_data:
				self.import_state.config(fg="red4", text="no data")
			else:
				self.import_state.config(text="")
			
			
			# Current:
			self.curr_dt.config(text= self.c_dt)
			self.curr_timezone.config(text= self.c_timezone)
			try:
				self.curr_dt_intimezone.config(text= self.c_dt_intimezone.strftime(lang[my_language]["hours_minutes2"]))
			except:
				self.curr_dt_intimezone.config(text= self.c_dt_intimezone)
			
			self.curr_temp.config(text= str(self.c_temp) + unit_temp2)
			self.curr_icon.config(image= self.c_icon)
			self.c_windvane = Image.open(img_dir + windvane(self.c_windspeed, self.c_winddeg)[0] + ".png")
			self.c_windvane = self.c_windvane.rotate(windvane(self.c_windspeed, self.c_winddeg)[1])
			self.c_windvane = self.c_windvane.resize((30, 30), Image.ANTIALIAS)
			self.c_windvane = ImageTk.PhotoImage(self.c_windvane)
			self.curr_windvane.config(image= self.c_windvane)
			self.curr_description.config(text= self.c_description)
			wind_description = lang[my_language]["wind_description"][convert_windspeed(self.c_windspeed)]
			wind_direction = lang[my_language]["wind_direction"][convert_winddeg(self.c_winddeg)]
			if type(self.c_winddeg) != float and type(self.c_winddeg) != int:
				self.curr_wind.config(text= wind_description)
			else:
				self.curr_wind.config(text= lang[my_language]["wind_format"].format(wind_description=wind_description, wind_direction=wind_direction))
			self.curr_sun.config(text= lang[my_language]["sunrise_sunset"].format(self.c_sunrise, self.c_sunset))
			#self.curr_pressure = Label(self.frame_current, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color, text="Luftdruck: "+str(self.c_pressure)+" hpa")
			self.curr_locname.config(text=str(self.c_locname) +", "+ str(self.c_country))
			self.curr_infolabel.config(
									text=
										lang[my_language]["clouds"].format(self.c_clouds) +"\n"+
										lang[my_language]["temp_rest_day"].format(max=self.c_temp_max, min=self.c_temp_min, u=unit_temp1) +"\n"+
										#lang[my_language]["wind_speed"].format(speed=self.c_windspeed, u=unit_speed) +"\n"+
										#lang[my_language]["visibility"].format(self.c_visibility) +"\n"+
										lang[my_language]["humidity"].format(self.c_humidity))#+"\n"+
										#"x"+"Niederschlag/Regenmenge..?" +"\n"+
			
		
		def update_widgets_hourlyforecast():
			# Next (hourly forecast):
			if hf == True:
				self.n1_time = self.n1_a_time
				self.n1_temp = self.n1_a_temp
				self.n1_iconid = self.n1_a_iconid
				self.n1_description = self.n1_a_description
				self.n1_clouds = self.n1_a_clouds
				self.n1_windspeed = self.n1_a_windspeed
				self.n1_winddeg = self.n1_a_winddeg
				self.n2_time = self.n2_a_time
				self.n2_temp = self.n2_a_temp
				self.n2_iconid = self.n2_a_iconid
				self.n2_description = self.n2_a_description
				self.n2_clouds = self.n2_a_clouds
				self.n2_windspeed = self.n2_a_windspeed
				self.n2_winddeg = self.n2_a_winddeg
				self.n3_time = self.n3_a_time
				self.n3_temp = self.n3_a_temp
				self.n3_iconid = self.n3_a_iconid
				self.n3_description = self.n3_a_description
				self.n3_clouds = self.n3_a_clouds
				self.n3_windspeed = self.n3_a_windspeed
				self.n3_winddeg = self.n3_a_winddeg
				self.button_switch_hf.config(image=self.button_switch_hf3_file)
			else:
				self.n1_time = self.n1_b_time
				self.n1_temp = self.n1_b_temp
				self.n1_iconid = self.n1_b_iconid
				self.n1_description = self.n1_b_description
				self.n1_clouds = self.n1_b_clouds
				self.n1_windspeed = self.n1_b_windspeed
				self.n1_winddeg = self.n1_b_winddeg
				self.n2_time = self.n2_b_time
				self.n2_temp = self.n2_b_temp
				self.n2_iconid = self.n2_b_iconid
				self.n2_description = self.n2_b_description
				self.n2_clouds = self.n2_b_clouds
				self.n2_windspeed = self.n2_b_windspeed
				self.n2_winddeg = self.n2_b_winddeg
				self.n3_time = self.n3_b_time
				self.n3_temp = self.n3_b_temp
				self.n3_iconid = self.n3_b_iconid
				self.n3_description = self.n3_b_description
				self.n3_clouds = self.n3_b_clouds
				self.n3_windspeed = self.n3_b_windspeed
				self.n3_winddeg = self.n3_b_winddeg
				self.button_switch_hf.config(image=self.button_switch_hf6_file)
				
			self.next1_time.config(text= str(self.n1_time) + lang[my_language]["hour"])
			self.next1_temp.config(text= str(self.n1_temp) + unit_temp1)
			self.n1_icon = Image.open(img_dir + self.n1_iconid + ".png")
			self.n1_icon = self.n1_icon.resize((45, 45), Image.ANTIALIAS)
			self.n1_icon = ImageTk.PhotoImage(self.n1_icon)
			self.next1_icon.config(image= self.n1_icon)
			#self.next1_description.config(text= self.n1_description)
			#self.next1_clouds.config(text= str(self.n1_clouds)+" % Bewölkung")
			#self.next1_wind.config(text= convert_windspeed(self.n1_windspeed) + unit_speed +"aus "+ convert_winddeg(self.n1_winddeg))
			self.n1_windvane = Image.open(img_dir + windvane(self.n1_windspeed, self.n1_winddeg)[0] + ".png")
			self.n1_windvane = self.n1_windvane.rotate(windvane(self.n1_windspeed, self.n1_winddeg)[1])
			self.n1_windvane = self.n1_windvane.resize((20, 20), Image.ANTIALIAS)
			self.n1_windvane = ImageTk.PhotoImage(self.n1_windvane)
			self.next1_windvane.config(image= self.n1_windvane)
			self.next1_infolabel.config(text=
											lang[my_language]["clouds2"].format(str(self.n1_clouds)) +"\n"+
											str(self.n1_windspeed) + unit_speed)
			
			
			self.next2_time.config(text= str(self.n2_time) + lang[my_language]["hour"])
			self.next2_temp.config(text= str(self.n2_temp) + unit_temp1)
			self.n2_icon = Image.open(img_dir + self.n2_iconid + ".png")
			self.n2_icon = self.n2_icon.resize((45, 45), Image.ANTIALIAS)
			self.n2_icon = ImageTk.PhotoImage(self.n2_icon)
			self.next2_icon.config(image= self.n2_icon)
			#self.next2_description.config(text= self.n2_description)
			#self.next2_clouds.config(text= str(self.n2_clouds)+" % Bewölkung")
			#self.next2_wind.config(text= convert_windspeed(self.n2_windspeed) + unit_speed +"aus "+ convert_winddeg(self.n2_winddeg))
			self.n2_windvane = Image.open(img_dir + windvane(self.n2_windspeed, self.n2_winddeg)[0] + ".png")
			self.n2_windvane = self.n2_windvane.rotate(windvane(self.n2_windspeed, self.n2_winddeg)[1])
			self.n2_windvane = self.n2_windvane.resize((20, 20), Image.ANTIALIAS)
			self.n2_windvane = ImageTk.PhotoImage(self.n2_windvane)
			self.next2_windvane.config(image= self.n2_windvane)
			self.next2_infolabel.config(text=
											lang[my_language]["clouds2"].format(str(self.n2_clouds)) +"\n"+
											str(self.n2_windspeed) + unit_speed)
			
			
			self.next3_time.config(text= str(self.n3_time) + lang[my_language]["hour"])
			self.next3_temp.config(text= str(self.n3_temp) + unit_temp1)
			self.n3_icon = Image.open(img_dir + self.n3_iconid + ".png")
			self.n3_icon = self.n3_icon.resize((45, 45), Image.ANTIALIAS)
			self.n3_icon = ImageTk.PhotoImage(self.n3_icon)	
			self.next3_icon.config(image= self.n3_icon)
			#self.next3_description.config(text= self.n3_description)
			#self.next3_clouds.config(text= str(self.n3_clouds)+" % Bewölkung")
			#self.next3_wind.config(text= convert_windspeed(self.n3_windspeed) + unit_speed +"aus "+ convert_winddeg(self.n3_winddeg))
			self.n3_windvane = Image.open(img_dir + windvane(self.n3_windspeed, self.n3_winddeg)[0] + ".png")
			self.n3_windvane = self.n3_windvane.rotate(windvane(self.n3_windspeed, self.n3_winddeg)[1])
			self.n3_windvane = self.n3_windvane.resize((20, 20), Image.ANTIALIAS)
			self.n3_windvane = ImageTk.PhotoImage(self.n3_windvane)
			self.next3_windvane.config(image= self.n3_windvane)
			self.next3_infolabel.config(text=
											lang[my_language]["clouds2"].format(str(self.n3_clouds)) +"\n"+
											str(self.n3_windspeed) + unit_speed)
		
		
		def update_widgets_nextday():
			# Next day:
			if self.n3_time < 13 or hf == True or self.n3_day == self.c_dt_intimezone.day: # Try/Except für self.c_dt_intimezone.day?
				#print (self.c_dt_intimezone.day)						# If self.c_dt_intimezone is not a datetime-Objekt yet, it won't have an attribute .day
				self.nextday.config(text= self.nday1)
				self.nday1_noon_icon = Image.open(img_dir + self.nday1_noon_iconid + ".png")
				self.nday1_noon_icon = self.nday1_noon_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday1_noon_icon = ImageTk.PhotoImage(self.nday1_noon_icon)
				self.nextday_icon.config(image= self.nday1_noon_icon)
				self.nextday_temp1.config(text= str(self.nday1_temp_max) + unit_temp1)
				self.nextday_temp2.config(text= "/  " + str(self.nday1_temp_min) + unit_temp1)

			elif self.n3_time >= 13 and hf == False:
				self.nextday.config(text= str(lang[my_language]["weekday"].get(str(self.nday2))) +":")
				self.nday2_noon_icon = Image.open(img_dir + self.nday2_noon_iconid + ".png")
				self.nday2_noon_icon = self.nday2_noon_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday2_noon_icon = ImageTk.PhotoImage(self.nday2_noon_icon)
				self.nextday_icon.config(image= self.nday2_noon_icon)
				self.nextday_temp1.config(text= str(self.nday2_temp_max) + unit_temp1)
				self.nextday_temp2.config(text= "/  " + str(self.nday2_temp_min) + unit_temp1)


		def update_widgets_nextdays():
			#Next days with daytimes:
			
			# NEXTDAY 1
			self.nextday1.config(text= self.nday1)
			self.nextday1_temp1.config(text= str(self.nday1_temp_max) + unit_temp1)
			self.nextday1_temp2.config(text= "/  " + str(self.nday1_temp_min) + unit_temp1)
			self.nextday1_night_temp.config(text= str(self.nday1_night_temp) + unit_temp1)
			if switch_view == 3:
				self.nday1_night_icon = Image.open(img_dir + self.nday1_night_iconid + ".png")
				self.nday1_night_icon = self.nday1_night_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday1_night_icon = ImageTk.PhotoImage(self.nday1_night_icon)
			self.nextday1_night_icon.config(image= self.nday1_night_icon)
			self.nday1_night_windvane = Image.open(img_dir + windvane(self.nday1_night_windspeed, self.nday1_night_winddeg)[0] + ".png")
			self.nday1_night_windvane = self.nday1_night_windvane.rotate(windvane(self.nday1_night_windspeed, self.nday1_night_winddeg)[1])
			self.nday1_night_windvane = self.nday1_night_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday1_night_windvane = ImageTk.PhotoImage(self.nday1_night_windvane)
			self.nextday1_night_windvane.config(image= self.nday1_night_windvane)
			#self.nextday1_night_infolabel.config(
			
			self.nextday1_morning_temp.config(text= str(self.nday1_morning_temp) + unit_temp1)
			if switch_view == 3:
				self.nday1_morning_icon = Image.open(img_dir + self.nday1_morning_iconid + ".png")
				self.nday1_morning_icon = self.nday1_morning_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday1_morning_icon = ImageTk.PhotoImage(self.nday1_morning_icon)
			self.nextday1_morning_icon.config(image= self.nday1_morning_icon)
			self.nday1_morning_windvane = Image.open(img_dir + windvane(self.nday1_morning_windspeed, self.nday1_morning_winddeg)[0] + ".png")
			self.nday1_morning_windvane = self.nday1_morning_windvane.rotate(windvane(self.nday1_morning_windspeed, self.nday1_morning_winddeg)[1])
			self.nday1_morning_windvane = self.nday1_morning_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday1_morning_windvane = ImageTk.PhotoImage(self.nday1_morning_windvane)
			self.nextday1_morning_windvane.config(image= self.nday1_morning_windvane)
			#self.nextday1_morning_infolabel
			
			self.nextday1_noon_temp.config(text= str(self.nday1_noon_temp) + unit_temp1)
			if switch_view == 3:
				self.nday1_noon_icon = Image.open(img_dir + self.nday1_noon_iconid + ".png")
				self.nday1_noon_icon = self.nday1_noon_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday1_noon_icon = ImageTk.PhotoImage(self.nday1_noon_icon)
			self.nextday1_noon_icon.config(image= self.nday1_noon_icon)
			self.nday1_noon_windvane = Image.open(img_dir + windvane(self.nday1_noon_windspeed, self.nday1_noon_winddeg)[0] + ".png")
			self.nday1_noon_windvane = self.nday1_noon_windvane.rotate(windvane(self.nday1_noon_windspeed, self.nday1_noon_winddeg)[1])
			self.nday1_noon_windvane = self.nday1_noon_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday1_noon_windvane = ImageTk.PhotoImage(self.nday1_noon_windvane)
			self.nextday1_noon_windvane.config(image= self.nday1_noon_windvane)
			#self.nextday1_noon_infolabel
			
			self.nextday1_evening_temp.config(text= str(self.nday1_evening_temp) + unit_temp1)
			if switch_view == 3:
				self.nday1_evening_icon = Image.open(img_dir + self.nday1_evening_iconid + ".png")
				self.nday1_evening_icon = self.nday1_evening_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday1_evening_icon = ImageTk.PhotoImage(self.nday1_evening_icon)
			self.nextday1_evening_icon.config(image= self.nday1_evening_icon)
			self.nday1_evening_windvane = Image.open(img_dir + windvane(self.nday1_evening_windspeed, self.nday1_evening_winddeg)[0] + ".png")
			self.nday1_evening_windvane = self.nday1_evening_windvane.rotate(windvane(self.nday1_evening_windspeed, self.nday1_evening_winddeg)[1])
			self.nday1_evening_windvane = self.nday1_evening_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday1_evening_windvane = ImageTk.PhotoImage(self.nday1_evening_windvane)
			self.nextday1_evening_windvane.config(image= self.nday1_evening_windvane)
			#self.nextday1_evening_infolabel
			
			
			#NEXTDAY 2
			self.nextday2.config(text= str(lang[my_language]["weekday"].get(str(self.nday2))) + ":")
			self.nextday2_temp1.config(text= str(self.nday2_temp_max) + unit_temp1)
			self.nextday2_temp2.config(text= "/  " + str(self.nday2_temp_min) + unit_temp1)
			self.nextday2_night_temp.config(text= str(self.nday2_night_temp) + unit_temp1)
			if switch_view == 3:
				self.nday2_night_icon = Image.open(img_dir + self.nday2_night_iconid + ".png")
				self.nday2_night_icon = self.nday2_night_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday2_night_icon = ImageTk.PhotoImage(self.nday2_night_icon)
			self.nextday2_night_icon.config(image= self.nday2_night_icon)
			self.nday2_night_windvane = Image.open(img_dir + windvane(self.nday2_night_windspeed, self.nday2_night_winddeg)[0] + ".png")
			self.nday2_night_windvane = self.nday2_night_windvane.rotate(windvane(self.nday2_night_windspeed, self.nday2_night_winddeg)[1])
			self.nday2_night_windvane = self.nday2_night_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday2_night_windvane = ImageTk.PhotoImage(self.nday2_night_windvane)
			self.nextday2_night_windvane.config(image= self.nday2_night_windvane)
			#self.nextday2_night_infolabel.config(
			
			self.nextday2_morning_temp.config(text= str(self.nday2_morning_temp) + unit_temp1)
			if switch_view == 3:
				self.nday2_morning_icon = Image.open(img_dir + self.nday2_morning_iconid + ".png")
				self.nday2_morning_icon = self.nday2_morning_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday2_morning_icon = ImageTk.PhotoImage(self.nday2_morning_icon)
			self.nextday2_morning_icon.config(image= self.nday2_morning_icon)
			self.nday2_morning_windvane = Image.open(img_dir + windvane(self.nday2_morning_windspeed, self.nday2_morning_winddeg)[0] + ".png")
			self.nday2_morning_windvane = self.nday2_morning_windvane.rotate(windvane(self.nday2_morning_windspeed, self.nday2_morning_winddeg)[1])
			self.nday2_morning_windvane = self.nday2_morning_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday2_morning_windvane = ImageTk.PhotoImage(self.nday2_morning_windvane)
			self.nextday2_morning_windvane.config(image= self.nday2_morning_windvane)
			#self.nextday2_morning_infolabel
			
			self.nextday2_noon_temp.config(text= str(self.nday2_noon_temp) + unit_temp1)
			if switch_view == 3:
				self.nday2_noon_icon = Image.open(img_dir + self.nday2_noon_iconid + ".png")
				self.nday2_noon_icon = self.nday2_noon_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday2_noon_icon = ImageTk.PhotoImage(self.nday2_noon_icon)
			self.nextday2_noon_icon.config(image= self.nday2_noon_icon)
			self.nday2_noon_windvane = Image.open(img_dir + windvane(self.nday2_noon_windspeed, self.nday2_noon_winddeg)[0] + ".png")
			self.nday2_noon_windvane = self.nday2_noon_windvane.rotate(windvane(self.nday2_noon_windspeed, self.nday2_noon_winddeg)[1])
			self.nday2_noon_windvane = self.nday2_noon_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday2_noon_windvane = ImageTk.PhotoImage(self.nday2_noon_windvane)
			self.nextday2_noon_windvane.config(image= self.nday2_noon_windvane)
			#self.nextday2_noon_infolabel
						
			self.nextday2_evening_temp.config(text= str(self.nday2_evening_temp) + unit_temp1)
			if switch_view == 3:
				self.nday2_evening_icon = Image.open(img_dir + self.nday2_evening_iconid + ".png")
				self.nday2_evening_icon = self.nday2_evening_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday2_evening_icon = ImageTk.PhotoImage(self.nday2_evening_icon)
			self.nextday2_evening_icon.config(image= self.nday2_evening_icon)
			self.nday2_evening_windvane = Image.open(img_dir + windvane(self.nday2_evening_windspeed, self.nday2_evening_winddeg)[0] + ".png")
			self.nday2_evening_windvane = self.nday2_evening_windvane.rotate(windvane(self.nday2_evening_windspeed, self.nday2_evening_winddeg)[1])
			self.nday2_evening_windvane = self.nday2_evening_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday2_evening_windvane = ImageTk.PhotoImage(self.nday2_evening_windvane)
			self.nextday2_evening_windvane.config(image= self.nday2_evening_windvane)
			#self.nextday2_evening_infolabel
			
			
			# NEXTDAY 3
			self.nextday3.config(text= str(lang[my_language]["weekday"].get(str(self.nday3))) + ":")
			self.nextday3_temp1.config(text= str(self.nday3_temp_max) + unit_temp1)
			self.nextday3_temp2.config(text= "/  " + str(self.nday3_temp_min) + unit_temp1)
			self.nextday3_night_temp.config(text= str(self.nday3_night_temp) + unit_temp1)
			if switch_view == 3:
				self.nday3_night_icon = Image.open(img_dir + self.nday3_night_iconid + ".png")
				self.nday3_night_icon = self.nday3_night_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday3_night_icon = ImageTk.PhotoImage(self.nday3_night_icon)
			self.nextday3_night_icon.config(image= self.nday3_night_icon)
			try:
				self.nday3_night_windvane = Image.open(img_dir + windvane(self.nday3_night_windspeed, self.nday3_night_winddeg)[0] + ".png")
				self.nday3_night_windvane = self.nday3_night_windvane.rotate(windvane(self.nday3_night_windspeed, self.nday3_night_winddeg)[1])
			except:
				self.nday3_night_windvane = Image.open(img_dir + "noinfo.png")
			self.nday3_night_windvane = self.nday3_night_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday3_night_windvane = ImageTk.PhotoImage(self.nday3_night_windvane)
			self.nextday3_night_windvane.config(image= self.nday3_night_windvane)
			#self.nextday3_night_infolabel.config(
			
			self.nextday3_morning_temp.config(text= str(self.nday3_morning_temp) + unit_temp1)
			if switch_view == 3:
				self.nday3_morning_icon = Image.open(img_dir + self.nday3_morning_iconid + ".png")
				self.nday3_morning_icon = self.nday3_morning_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday3_morning_icon = ImageTk.PhotoImage(self.nday3_morning_icon)
			self.nextday3_morning_icon.config(image= self.nday3_morning_icon)
			self.nday3_morning_windvane = Image.open(img_dir + windvane(self.nday3_morning_windspeed, self.nday3_morning_winddeg)[0] + ".png")
			self.nday3_morning_windvane = self.nday3_morning_windvane.rotate(windvane(self.nday3_morning_windspeed, self.nday3_morning_winddeg)[1])
			self.nday3_morning_windvane = self.nday3_morning_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday3_morning_windvane = ImageTk.PhotoImage(self.nday3_morning_windvane)
			self.nextday3_morning_windvane.config(image= self.nday3_morning_windvane)
			#self.nextday3_morning_infolabel
			
			self.nextday3_noon_temp.config(text= str(self.nday3_noon_temp) + unit_temp1)
			if switch_view == 3:
				self.nday3_noon_icon = Image.open(img_dir + self.nday3_noon_iconid + ".png")
				self.nday3_noon_icon = self.nday3_noon_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday3_noon_icon = ImageTk.PhotoImage(self.nday3_noon_icon)
			self.nextday3_noon_icon.config(image= self.nday3_noon_icon)
			self.nday3_noon_windvane = Image.open(img_dir + windvane(self.nday3_noon_windspeed, self.nday3_noon_winddeg)[0] + ".png")
			self.nday3_noon_windvane = self.nday3_noon_windvane.rotate(windvane(self.nday3_noon_windspeed, self.nday3_noon_winddeg)[1])
			self.nday3_noon_windvane = self.nday3_noon_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday3_noon_windvane = ImageTk.PhotoImage(self.nday3_noon_windvane)
			self.nextday3_noon_windvane.config(image= self.nday3_noon_windvane)
			#self.nextday3_noon_infolabel
						
			self.nextday3_evening_temp.config(text= str(self.nday3_evening_temp) + unit_temp1)
			if switch_view == 3:
				self.nday3_evening_icon = Image.open(img_dir + self.nday3_evening_iconid + ".png")
				self.nday3_evening_icon = self.nday3_evening_icon.resize((40, 40), Image.ANTIALIAS)
				self.nday3_evening_icon = ImageTk.PhotoImage(self.nday3_evening_icon)
			self.nextday3_evening_icon.config(image= self.nday3_evening_icon)
			self.nday3_evening_windvane = Image.open(img_dir + windvane(self.nday3_evening_windspeed, self.nday3_evening_winddeg)[0] + ".png")
			self.nday3_evening_windvane = self.nday3_evening_windvane.rotate(windvane(self.nday3_evening_windspeed, self.nday3_evening_winddeg)[1])
			self.nday3_evening_windvane = self.nday3_evening_windvane.resize((16, 16), Image.ANTIALIAS)
			self.nday3_evening_windvane = ImageTk.PhotoImage(self.nday3_evening_windvane)
			self.nextday3_evening_windvane.config(image= self.nday3_evening_windvane)
			#self.nextday3_evening_infolabel
			
				
		update_widgets_current()
		update_widgets_hourlyforecast()
		update_widgets_nextday()
		update_widgets_nextdays()



class SettingsAndImport:
	
	def __init__(self):
		
		self.frame0 = Frame(window, bg=main_bg_color)		# frame_settings will be destroyed, frame0 has to continue existing because of import_data and timeout loops.
		self.iploc = Radiobutton(self.frame0)
		self.search_button = Button(self.frame0)
		
		
		self.err_state = False
		self.error_messages = ""
		self.to = False
		
		self.my_apikey = None
		self.my_location = None
		global my_language
		self.my_units = None
		self.app_settings = {}
		
		try:
			with open(saved_settings, "r") as f:
				self.app_settings = json.load(f)
			
			# Key, language, units and URL settings:
			self.my_apikey = self.app_settings.get("apikey")
			self.my_location = self.app_settings.get("location")
			my_language = self.app_settings.get("language")
			self.my_units = self.app_settings.get("units")
			
			self.loading_successful = True
			
			self.import_data() # Falls in self.import_data() ein Fehler auftritt, wird dieser durch die try:-Methode kaschiert! Wenn self.import_data() scheitert, geht es weiter mit except.
		
		except:
			# Open Settings to configure Weather app
			self.loading_successful = False
		
	
	def import_data(self, *args):
		
		def timeout():
			self.to = not self.to
			if self.to == True:
				self.search_button.config(state=DISABLED, cursor="arrow")
				window.bind_class("Entry", "<Return>", lambda e: None)
				self.iploc.unbind("<Return>")
				window.unbind("r")
				self.frame0.after(5000, timeout)
			else:
				self.search_button.config(state=NORMAL, cursor="hand2")
				window.bind_class("Entry", "<Return>", self.get_input)
				self.iploc.bind("<Return>", self.get_input)
				window.bind("r", settings_and_import.import_data)
			
		
		try:					# try becaue maybe the update_data loop doesn't exist yet.
			self.frame0.after_cancel(self.update_loop)
		except:
			pass
		
		global current_data
		global forecast_data
		global offline_state
		global no_data
		global c_dt
		global my_language
		global unit_temp1
		global unit_temp2
		global unit_speed
		
		if not self.my_units:
			self.my_units = "metric"
		if not self.my_apikey:
			self.error_messages += "API-Key fehlt\n"
			#self.settings_gui()
			self.err_state = True
		if not self.my_location:
			self.error_messages += "Ortsangabe fehlt\n"
			self.err_state = True
		
		if lang_import_failed:
			my_language = "en"
			
		if self.my_apikey and self.my_location:
		
			self.url_current_weather = ("http://api.openweathermap.org/data/2.5/weather?" +
										self.my_location +
										"&units=" +
										self.my_units +
										"&lang=" +
										my_language +
										"&APPID=" +
										self.my_apikey)
			self.url_forecast_weather = ("http://api.openweathermap.org/data/2.5/forecast?" +
										self.my_location +
										"&units=" +
										self.my_units +
										"&lang=" +
										my_language +
										"&APPID=" +
										self.my_apikey)
			current_data = {}
			forecast_data = {}
			offline_state = False
			no_data = True
			
			weather_app.import_state.config(fg="orange", text="import") # not shown for some reason :/
			
			timeout()
			
			try:
				with urlopen(self.url_current_weather) as f:
					current_data = eval(f.read()) # or with json?
					c_dt = tme.strftime("%H:%M", tme.localtime(current_data.get("dt")))
					print ("urlopen success:", tme.ctime())
				
				tme.sleep(0.5)
				
				with urlopen(self.url_forecast_weather) as g:
					forecast_data = eval(g.read()) # or with json?
					print ("urlopen success:", tme.ctime()), print("--")
				self.err_state = False
				no_data = False
			
			except error.URLError as err:	# Also HTTPError is covered.	# I am sure it's not Python2-compatible.
				print ("Error:", tme.ctime()), print (err), print("--")
				self.err_state = True
								
				if err.reason == "Not Found":
					self.error_messages += lang[my_language]["error"] + err.reason + '"\n\n' + self.my_location +"\n"+ lang[my_language]["not_found"]
				elif err.reason == "Unauthorized":
					self.error_messages += lang[my_language]["error"] + err.reason + '"\n\n' + lang[my_language]["unauthorized"]
				else:
					self.error_messages += str(err) + "\n\n" + lang[my_language]["connection"]
					offline_state = True
			
			except BaseException as err: 		# BaseException (Build-in Exception) would cover all exception errors of url.error (?) and more 	# Not Python2-compatible?
				print ("Error:", tme.ctime()), print (err), print("--")
				self.err_state = True
				self.error_messages += str(err)
				
			except: 		
				print ("Error:", tme.ctime()), print ("Something went wrong :/"), print("--")
				self.error_messages += lang[my_language]["other"]
				self.err_state = True
			
		
		if self.my_units == "imperial":
			unit_temp1 = "°"
			unit_temp2 = "°F"
			unit_speed = " mph"
		elif self.my_units == "metric":
			unit_temp1 = "°"
			unit_temp2 = "°C"
			unit_speed = " m/s"
		else:
			unit_temp1 = ""
			unit_temp2 = " K"
			unit_speed = " m/s"
		
		
		if not self.err_state:
			self.error_messages = ""
		
		if not self.err_state or offline_state:
			weather_app.update_data()
			self.update_loop = self.frame0.after(600000, self.import_data)
		
		else:
			self.loading_successful = False
		
	
	def settings_gui(self):
		
		def open_webpage(event):
			webbrowser.open_new(r"https://home.openweathermap.org/users/sign_up")
			
		
		def place_entry():
			rb = self.v.get()
			if rb==1:
				self.cityname_entry.grid(row=0, column=1, sticky=W)
				self.countrycode_entry.grid(row=0, column=2, padx=4, sticky=W)
				self.cityname_entry.focus_set()
				self.cityname.config(fg=main_fg_color, text=lang[my_language]["city_name"]+":")
				self.select_rb = 1
			else:
				self.cityname_entry.grid_forget()
				self.countrycode_entry.grid_forget()
				self.cityname.config(fg="grey", text=lang[my_language]["city_name"])
			if rb==2:
				self.zipcode_entry.grid(row=0, column=1, sticky=W)
				self.zipcode_cc_entry.grid(row=0, column=2, padx=4, sticky=W)
				self.zipcode_entry.focus_set()
				self.zipcode.config(fg=main_fg_color, text=lang[my_language]["zip"]+":")
				self.select_rb = 2
			else:
				self.zipcode_entry.grid_forget()
				self.zipcode_cc_entry.grid_forget()
				self.zipcode.config(fg="grey", text=lang[my_language]["zip"])
			if rb==3:
				self.cityid_entry.grid(row=0, column=1, sticky=W)
				self.cityid_entry.focus_set()
				self.cityid.config(fg=main_fg_color, text=lang[my_language]["cityid"]+":")
				self.select_rb = 3
			else:
				self.cityid_entry.grid_forget()
				self.cityid.config(fg="grey", text=lang[my_language]["cityid"])
			if rb==4:
				self.geocoor_entry_lat.grid(row=0, column=1, sticky=W)
				self.geocoor_entry_lon.grid(row=0, column=2, padx=4, sticky=W)
				self.geocoor_entry_lat.focus_set()
				self.geocoor.config(fg=main_fg_color, text="Lat. / Long.:")
				self.select_rb = 4
			else:
				self.geocoor_entry_lat.grid_forget()
				self.geocoor_entry_lon.grid_forget()
				self.geocoor.config(fg="grey", text="Lat. / Long.")
			if rb==5:
				self.iploc.config(fg=main_fg_color)
				self.iploc.focus_set()
				self.iploc_info.grid(row=0, column=1, sticky=W)
				self.select_rb = 5
			else:
				self.iploc.config(fg="grey")
				self.iploc_info.grid_forget()
				
		
		def switch_radiobutton(event):
			if event.keysym == "Up":
				self.select_rb -= 1
				if self.select_rb == 0:
					self.select_rb = 5
				self.v.set(self.select_rb)
				
			if event.keysym == "Down":
				self.select_rb += 1
				if self.select_rb == 6:
					self.select_rb = 1
				self.v.set(self.select_rb)
			place_entry()
			
		
		
		self.select_rb = 3
		self.v = IntVar()
		self.v.set(self.select_rb)
		
		global my_language
		self.sct_lang = StringVar()		 	# OptionMenu-Widget am besten ganz austauschen (POTTHÄSSLICH)
		if not my_language:
			self.sct_lang.set("en")
		else:
			self.sct_lang.set(my_language)
		
		self.sct_units = StringVar()
		if self.my_units == "standard":
			self.sct_units.set("K")
		elif self.my_units == "imperial":
			self.sct_units.set("°F")
		else:
			self.sct_units.set("°C")
		
		
		self.frame_settings = Frame(self.frame0, bg=main_bg_color)
		self.search_button = Button(self.frame0, font=(set_font, 10), text=lang[my_language]["search"], cursor="hand2")
		
		
		self.title = Label(window, font=(set_font, 12, "bold"), fg=main_fg_color, bg=main_bg_color, text=lang[my_language]["settings"], anchor=W)
		self.frame_apikey = Frame(self.frame_settings, bg=main_bg_color) #, borderwidth=1, relief="ridge")
		self.loc_insert_title = Label(self.frame_settings, font=(set_font, 8), text=lang[my_language]["search_by"], fg="grey", bg=main_bg_color)
		self.frame_loc_insert = Frame(self.frame_settings, bg=main_bg_color)
		self.frame_lang_units = Frame(self.frame_settings, bg=main_bg_color)
		self.loc_result = Message(self.frame_settings, font=set_font+" 8", fg=main_fg_color, bg=main_bg_color, justify=CENTER, width=340)
		
		self.frame0.place(relx=0.5, rely=0.5, width=440, height=255, y=-115, anchor=N)
		self.title.place(relx=0.5, rely=0.5, height=25, x=-220, y=-150, relwidth=0.75, anchor=NW)
		self.frame_settings.place(relx=0, rely=0, relwidth=1, relheight=1, anchor=NW)
		#settings_and_import.title.lift(weather_app.frame0)
		#self.frame_settings.lift(uhr.frame0)
		#self.frame_settings.lift(weather_app.frame0) # Es sollte aber reichen:
		self.frame0.lift() # Falls überhaupt noch notwendig, wenn self.frame_settings bei Aufrufen von settings_gui immer wieder gezeichnet wird
		
		
		self.frame_apikey.pack(pady=5, anchor=W)
		self.loc_insert_title.pack(anchor=W)
		self.frame_loc_insert.pack(anchor=W, fill=X)
		self.frame_lang_units.place(relx=1, rely=0.5, anchor=E)
		self.loc_result.pack(pady=5)
		
		self.apikey = Label(self.frame_apikey, font=(set_font, 10), text=lang[my_language]["api_key"]+":", fg=main_fg_color, bg=main_bg_color)
		self.apikey_entry =Entry(self.frame_apikey, font=(set_font, 10), width=33, bg=main_fg_color)
		if self.my_apikey:
			self.apikey_entry.insert(0, self.my_apikey)
		self.apikey_request = Label(self.frame_apikey, font=(set_font, 8), cursor="hand2", text=lang[my_language]["get_key"], fg="grey", bg=main_bg_color)
		self.apikey_request.bind("<1>", open_webpage)
		
		self.loc_ins1 = Frame(self.frame_loc_insert, bg=main_bg_color)
		self.loc_ins2 = Frame(self.frame_loc_insert, bg=main_bg_color)
		self.loc_ins3 = Frame(self.frame_loc_insert, bg=main_bg_color)
		self.loc_ins4 = Frame(self.frame_loc_insert, bg=main_bg_color)
		self.loc_ins5 = Frame(self.frame_loc_insert, bg=main_bg_color)
		
		self.cityname = Radiobutton(self.loc_ins1, font=(set_font, 9), cursor="hand2", variable=self.v, value=1, command=place_entry, bg=main_bg_color, fg="grey", text=lang[my_language]["city_name"], selectcolor="black")
		self.zipcode = Radiobutton(self.loc_ins2, font=(set_font, 9), cursor="hand2", variable=self.v, value=2, command=place_entry, bg=main_bg_color, fg="grey", text=lang[my_language]["zip"], selectcolor="black")
		self.cityid = Radiobutton(self.loc_ins3, font=(set_font, 9), cursor="hand2", variable=self.v, value=3, command=place_entry, bg=main_bg_color, fg=main_fg_color, text=lang[my_language]["cityid"]+":", selectcolor="black")
		self.geocoor = Radiobutton(self.loc_ins4, font=(set_font, 9), cursor="hand2", variable=self.v, value=4, command=place_entry,bg=main_bg_color, fg="grey", text="Lat. / Long.", selectcolor="black")
		self.iploc = Radiobutton(self.loc_ins5, font=(set_font, 9), cursor="hand2", variable=self.v, value=5, command=place_entry, bg=main_bg_color, fg="grey", text=lang[my_language]["auto"], selectcolor="black")#, state="disabled")
		window.bind("<Up>", switch_radiobutton)
		window.bind("<Down>", switch_radiobutton)
		
		self.cityname_entry = Entry(self.loc_ins1, font=(set_font, 9), width=25, bg=main_fg_color) # There is a french town with a name of 34 chars in the city list of openweathermap
		self.countrycode_entry = Entry(self.loc_ins1, font=(set_font, 9), width=3, bg=main_fg_color)
		self.zipcode_entry = Entry(self.loc_ins2, font=(set_font, 9), width=6, bg=main_fg_color)
		self.zipcode_cc_entry = Entry(self.loc_ins2, font=(set_font, 9), width=3, bg=main_fg_color)
		self.cityid_entry = Entry(self.loc_ins3, font=(set_font, 9), width=10, bg=main_fg_color)
		self.geocoor_entry_lat = Entry(self.loc_ins4, font=(set_font, 9), width=11, bg=main_fg_color)
		self.geocoor_entry_lon = Entry(self.loc_ins4, font=(set_font, 9), width=11, bg=main_fg_color)
		self.iploc_info = Label(self.loc_ins5, font=(set_font, 8), bg=main_bg_color)
		
		if not self.to:
			window.bind_class("Entry", "<Return>", self.get_input)
			self.iploc.bind("<Return>", self.get_input)
		else:
			window.bind_class("Entry", "<Return>", lambda e: None)
			self.search_button.config(state=DISABLED)
			self.iploc.unbind("<Return>")
			
		# window.bind_class("Radiobutton", "<Return>", place_entry) # nicht nötig denke ich
		
		self.select_language = OptionMenu(*(self.frame_lang_units, self.sct_lang) + tuple(lang)) # HÄSSLICH
		self.select_units = OptionMenu(self.frame_lang_units, self.sct_units, "K", "°F", "°C")
				
		self.apikey.grid(row=0, column=0, sticky=W)
		self.apikey_entry.grid(row=0, column=1, padx=5)
		self.apikey_request.grid(row=0, column=2)
		
		self.loc_ins1.pack(anchor=W)
		self.loc_ins2.pack(anchor=W)
		self.loc_ins3.pack(anchor=W)
		self.loc_ins4.pack(anchor=W)
		self.loc_ins5.pack(anchor=W)
		
		self.cityname.grid(row=0, column=0, sticky=W)
		self.zipcode.grid(row=0, column=0, sticky=W)
		self.cityid.grid(row=0, column=0, sticky=W)
		self.geocoor.grid(row=0, column=0, sticky=W)
		self.iploc.grid(row=0, column=0, sticky=W)
		self.select_language.pack()
		self.select_units.pack()
		
		self.cityid_entry.grid(row=0, column=1, sticky=W)
		self.cityid.select()
		
		if not self.my_apikey:
			self.apikey_entry.focus_set()
		else:
			self.cityid_entry.focus_set()
		
		self.search_button.config(command=self.get_input)
		self.search_button.place(relx=0, rely=1, anchor=SW)
		
		self.show_result()
		

	def get_input(self, *args):
		self.err_state = False
		global my_language
		rb = self.v.get()
		self.error_messages = ""
		self.loc_result.config(fg=main_fg_color, text= self.error_messages)
		self.iploc_info.config(text="")
		
		if rb==1:
			if self.cityname_entry.get() == "":
				self.my_location = None
			else:
				if self.countrycode_entry.get() == "":
					self.my_location = "q="+ quote(self.cityname_entry.get().strip())
				else:
					self.my_location = "q="+ quote(self.cityname_entry.get().strip()) +","+ self.countrycode_entry.get().strip()
		if rb==2:
			if self.zipcode_entry.get() == "":
				self.my_location = None
			else:
				if not self.zipcode_cc_entry.get().isalpha():
					self.my_location = "zip="+ self.zipcode_entry.get().strip()
				else:
					self.my_location = "zip="+ self.zipcode_entry.get().strip() +","+ self.zipcode_cc_entry.get().strip()
		if rb==3:
			if not self.cityid_entry.get().isdigit():
				self.my_location = None
				self.error_messages += lang[my_language]["numbers"]+"\n\n"
			else:
				self.my_location = "id="+ self.cityid_entry.get().strip()
		if rb==4:
			if self.geocoor_entry_lat.get() == "" or self.geocoor_entry_lon.get() == "":
				self.my_location = None	
			else:
				self.my_location = "lat="+ self.geocoor_entry_lat.get().strip() +"&lon="+ self.geocoor_entry_lon.get().strip()
		if rb==5:
			ip_api = {}
			try:
				with urlopen("http://ip-api.com/json") as f:
					ip_api = eval(f.read())
			except:		#optional: Exception handling
				self.my_location = None
				self.error_messages += lang[my_language]["other"]
				self.iploc_info.config(text="failed", fg="red")
			if "lat" in ip_api and "lon" in ip_api:
				self.my_location = "lat="+ str(ip_api["lat"]) +"&lon="+ str(ip_api["lon"])
				print("Find IP location:", ip_api.get("status"))
				self.iploc_info.config(text=ip_api.get("status"), fg="green")
			elif "message" in ip_api:
				self.error_messages += ip_api["message"]
				self.iploc_info.config(text="failed", fg="green")
				self.my_location = None
			
				
		self.my_apikey = self.apikey_entry.get().strip()
		if not self.my_apikey:
			self.error_messages += lang[my_language]["api_missing"] +"\n"
			self.err_state = True
			self.apikey_entry.focus_set()
		
		if not self.my_location:
			self.error_messages += lang[my_language]["place_missing"] +"\n"
			self.err_state = True
			self.cityid_entry.focus_set()
		
		
		my_language = self.sct_lang.get()
		self.my_units = self.sct_units.get()
		if self.my_units == "K":
			self.my_units = "standard"
		elif self.my_units == "°F":
			self.my_units = "imperial"
		else:
			self.my_units = "metric"
		
		
		if self.my_location and self.my_apikey:
			self.app_settings = {}
			self.app_settings["apikey"] = self.my_apikey
			self.app_settings["location"] = self.my_location
			self.app_settings["language"] = my_language
			self.app_settings["units"] = self.my_units
			self.app_settings = json.dumps(self.app_settings)
			try:
				with open(saved_settings, "w") as f:
					f.write(self.app_settings)
			except:
				self.loc_result.config(fg="red4", text= lang[my_language]["write_save"])
			
			
			self.import_data()
			self.show_result()
			
			self.cityid.focus_set() # To remove focus from apikey_entry or self.cityid_entry.focus_set()
			
			self.cityname_entry.delete(0, END)
			self.countrycode_entry.delete(0, END)
			self.zipcode_entry.delete(0, END)
			self.zipcode_cc_entry.delete(0, END)
			self.cityid_entry.delete(0, END)
			self.geocoor_entry_lat.delete(0, END)
			self.geocoor_entry_lon.delete(0, END)
			self.cityname_entry.grid_forget()
			self.countrycode_entry.grid_forget()
			self.zipcode_entry.grid_forget()
			self.zipcode_cc_entry.grid_forget()
			self.cityid_entry.grid_forget()
			self.geocoor_entry_lat.grid_forget()
			self.geocoor_entry_lon.grid_forget()
			
		else:
			self.show_result()
		
		
	def show_result(self):
		
		if "sys" in current_data and self.err_state == False:
			self.loc_result.config(fg=main_fg_color, text=
														weather_app.c_locname +", "+ weather_app.c_country +"\n"+
														lang[my_language]["cityid"]+": "+ str(weather_app.c_cityid) +"\n"+
														"Lat: "+ str(weather_app.c_lat) +" | "+ "Lon: "+ str(weather_app.c_lon) +"\n"+
														lang[my_language]["timezone"]+": "+ weather_app.c_zone_timezone + " (" + weather_app.c_timezone +")")
		else:
			self.loc_result.config(fg="red4", text= self.error_messages)
		


class KeyControl:
	
	def __init__(self):
		
		self.frame0 = Frame(window, bg=main_bg_color)
		self.frame0.place(relx=0.5, rely=0.5, width=474, height=314, x=+237, y=-157, anchor=NE) # width= 220, height=25 (width 216 to match with forecast-frame.) height=35
		
		self.button_settings_file = Image.open(img_dir + "Buttons/button_settings_1-d.png")
		self.button_settings_file = self.button_settings_file.resize((17,17), Image.ANTIALIAS)
		self.button_settings_file = ImageTk.PhotoImage(self.button_settings_file)
		self.button_help_file = Image.open(img_dir + "Buttons/button_help.png")
		self.button_help_file = self.button_help_file.resize((18,18), Image.ANTIALIAS)
		self.button_help_file = ImageTk.PhotoImage(self.button_help_file)
		self.button_quit_file = Image.open(img_dir + "Buttons/button_quit.png")
		self.button_quit_file = self.button_quit_file.resize((17,17), Image.ANTIALIAS)
		self.button_quit_file = ImageTk.PhotoImage(self.button_quit_file)
		self.button_close_app_file = Image.open(img_dir + "Buttons/button_quit-d.png")
		self.button_close_app_file = self.button_close_app_file.resize((19,19), Image.ANTIALIAS)
		self.button_close_app_file = ImageTk.PhotoImage(self.button_close_app_file)
		self.button_sv_l_file = Image.open(img_dir + "Buttons/Arrow4.png")
		self.button_sv_l_file = self.button_sv_l_file.transpose(Image.FLIP_LEFT_RIGHT)
		self.button_sv_l_file = self.button_sv_l_file.resize((32,32), Image.ANTIALIAS)
		self.button_sv_l_file = ImageTk.PhotoImage(self.button_sv_l_file)
		self.button_sv_r_file = Image.open(img_dir + "Buttons/Arrow4.png")
		self.button_sv_r_file = self.button_sv_r_file.resize((32,32), Image.ANTIALIAS)
		self.button_sv_r_file = ImageTk.PhotoImage(self.button_sv_r_file)
		
		
		self.button_sv_r = Label(self.frame0, image=self.button_sv_r_file, bg=main_bg_color, cursor="hand2")
		self.button_sv_l = Label(self.frame0, image=self.button_sv_l_file, bg=main_bg_color, cursor="hand2") #activebackground=main_bg_color
		self.button_settings = Label(self.frame0, image=self.button_settings_file, bg=main_bg_color, cursor="hand2")
		self.button_help = Label(self.frame0, image=self.button_help_file, bg=main_bg_color, cursor="hand2")
		self.button_close_app = Label(self.frame0, image=self.button_close_app_file, bg=main_bg_color, cursor="hand2")
				
		self.button_sv_l.place(relx=1, x=-120, rely=0, y=+21, anchor=W)
		self.button_sv_r.place(relx=1, x=-120+40, rely=0, y=+21, anchor=W)
		self.button_settings.place(relx=1, rely=1, anchor=SE)
		self.button_close_app.place(relx=1, rely=0, anchor=NE)
		
		self.button_settings.bind("<1>", self.open_settings)
		self.button_help.bind("<1>", self.open_help)
		self.button_sv_r.bind("<1>", self.switch_view_r)
		self.button_sv_l.bind("<1>", self.switch_view_l)
		self.button_close_app.bind("<1>", self.exit_infobox)
		weather_app.button_switch_hf.bind("<1>", self.switch_hf)
		window.bind("<Return>", self.show_hide)
		window.bind("<Right>", self.switch_view_r)
		window.bind("<Left>", self.switch_view_l)
		window.bind("<Escape>", self.esc_fullscreen)
		window.bind("<F11>", self.toggle_fullscreen)
		window.bind("f", self.toggle_fullscreen)
		window.bind("s", self.open_settings)
		#window.bind("<Button-1>", self.show_mouse)
		#window.bind("<ButtonRelease-1>", self.hide_mouse)
		window.bind("<Double-Button-1>", self.show_hide)
		window.bind("6", self.hf6)
		window.bind("<Next>", self.hf6)
		window.bind("3", self.hf3)
		window.bind("<Prior>", self.hf3)
		window.bind("h", self.open_help)
		window.bind("r", settings_and_import.import_data)
		
		self.frame0.lower(weather_app.frame0)
		self.frame0.lower(uhr.frame0)
		
		
		self.state_fs = False
		global switch_view
		switch_view = 1
		self.state_sh = True
		self.state_help =False
		
		if settings_and_import.loading_successful == False:
			self.open_settings()
		
	
	def exit_infobox(self, event):
		window.destroy()
		# backframe.destroy()			# Win sys transparency test
		#sys.exit() # crashing, why?
		
	def open_settings(self, *args):
		self.button_sv_r.place_forget()
		self.button_sv_l.place_forget()
		self.button_close_app.place_forget()
		#window.unbind_all("<Double-Button-1>")
		window.unbind("<Double-Button-1>")	# or window.bind(event, lambda e: None)
		window.unbind("<Escape>")
		window.unbind("<Right>")
		window.unbind("<Left>")
		window.unbind("<Return>")
		window.unbind("f")
		window.unbind("s")
		window.unbind("6")
		window.unbind("3")
		window.unbind("h")
		window.unbind("r")	# Error? When opening settings "r" won't be unbinded every time!
		window["cursor"] = "arrow"

		self.button_settings.config(image=self.button_quit_file)
		self.button_settings.place(relx=1, rely=0, y=+22, x=-17, anchor=E)
		self.button_settings.bind("<1>", self.close_settings)
		self.button_help.place(relx=1, rely=0, y=+22, x=-60, anchor=E)
		window.bind("<Escape>", self.close_settings)
		settings_and_import.settings_gui()
	
	def close_settings(self, *args):
		settings_and_import.title.place_forget()
		settings_and_import.frame_settings.destroy()
		settings_and_import.iploc = Radiobutton(settings_and_import.frame0)
		settings_and_import.frame0.lower()
		self.button_sv_l.place(relx=1, x=-120, rely=0, y=+21, anchor=W)
		self.button_sv_r.place(relx=1, x=-120+40, rely=0, y=+21, anchor=W)
		self.button_close_app.place(relx=1, rely=0, anchor=NE)
		window.bind("<Double-Button-1>", self.show_hide)
		window.unbind("<Escape>")
		window.bind("<Escape>", self.esc_fullscreen)
		window.bind("<Right>", self.switch_view_r)
		window.bind("<Left>", self.switch_view_l)
		window.bind("<Return>", self.show_hide)
		window.bind("f", self.toggle_fullscreen)
		window.bind("s", self.open_settings)
		window.bind("6", self.hf6)
		window.bind("3", self.hf3)
		window.bind("h", self.open_help)
		window.bind("r", settings_and_import.import_data)
		window.unbind("<Up>")
		window.unbind("<Down>")
		self.button_settings.config(image=self.button_settings_file)
		self.button_settings.place(relx=1, rely=1, anchor=SE) # Why does it not show the Label again?
		self.button_settings.bind("<1>", self.open_settings)
		self.button_help.place_forget()
		self.state_sh = True
		
	
	def toggle_fullscreen(self, event):
		self.state_fs = not self.state_fs
		window.attributes("-fullscreen", self.state_fs)

	def esc_fullscreen(self, event):
		window.attributes("-fullscreen", False)
	
	def show_hide(self, event):
		self.state_sh = not self.state_sh
		if self.state_sh == False:
			window["cursor"] = "none"
			self.button_sv_r.place_forget()
			self.button_sv_l.place_forget()
			self.button_settings.place_forget()
			self.button_close_app.place_forget()
		else:
			#window["cursor"] = "plus"
			window["cursor"] = "arrow"
			self.button_sv_l.place(relx=1, x=-120, rely=0, y=+21, anchor=W)
			self.button_sv_r.place(relx=1, x=-120+40, rely=0, y=+21, anchor=W)
			self.button_settings.place(relx=1, rely=1, anchor=SE)
			self.button_close_app.place(relx=1, rely=0, anchor=NE)
			
	def switch_view_r(self, *args):
		global switch_view
		switch_view += 1
		if switch_view == 4:
			switch_view = 1
		if switch_view == 1:
			uhr.layout1()
			weather_app.layout1()
		if switch_view == 2:
			uhr.layout2()
			weather_app.layout2()
		if switch_view == 3:
			uhr.layout2()
			weather_app.layout3()
	def switch_view_l(self, *args):
		global switch_view
		switch_view -= 1
		if switch_view == 0:
			switch_view = 3
		if switch_view == 1:
			uhr.layout1()
			weather_app.layout1()
		if switch_view == 2:
			uhr.layout2()
			weather_app.layout2()
		if switch_view == 3:
			uhr.layout2()
			weather_app.layout3()
	
	def switch_hf(self, event):
		global hf
		hf = not hf
		weather_app.update_widgets()
		
	def hf3(self, peter):
		global hf
		hf = True
		weather_app.update_widgets()
	def hf6(self, paul):
		global hf
		hf = False
		weather_app.update_widgets()
	
	def open_help(self, *args):
		self.state_help = not self.state_help
		if self.state_help:
			help_and_credits.open_help()
		else:
			help_and_credits.close_help()
			
	

class HelpAndCredits:

	def __init__(self):
		self.font_size1 = 9
		self.font_size2 = 8
	
	
	def open_help(self):
		def open_webpage(event):
			webbrowser.open_new(r"https://github.com/jiavu")
		
		self.help_page = Toplevel()
		self.help_page.title("Infobox "+ infobox_version +"- Hilfe")
		self.help_page.config(bg=main_bg_color)
		
		#print(self.help_page.winfo_reqwidth())
		#print(self.help_page.winfo_reqheight())
		#self.help_page.geometry("%dx%d%+d%+d" % (self.help_page.winfo_reqwidth(), self.help_page.winfo_reqheight(), window.winfo_rootx(), window.winfo_rooty()))
				
		self.help_page.resizable(width=False, height=False)
		
		self.hotkeys = Frame(self.help_page, bg=main_bg_color, relief=GROOVE, bd=1)
		self.hotkeys1 = Label(self.hotkeys, bg=main_bg_color, fg="grey", font=(set_font, self.font_size1))
		self.hotkeys2 = Label(self.hotkeys, bg=main_bg_color, fg=main_fg_color, font=(set_font, self.font_size1), justify=LEFT)
		self.credits = Frame(self.help_page, bg=main_bg_color)
		self.credits1 = Label(self.credits, bg=main_bg_color, fg="grey", font=(set_font, 8))
		self.credits_linkedname = Label(self.credits, bg=main_bg_color, fg="grey65", font=(set_font, 8), cursor="hand2")
		self.credits2 = Label(self.credits, bg=main_bg_color, fg="grey", font=(set_font, 8))
		self.close = Button(self.help_page, font=(set_font, 8), text=lang[my_language]["close"], command=self.close_help)
		self.close.bind("<Return>", self.close_help)
		self.close.focus_set()
		self.help_page.bind("<Escape>", self.close_help)
		self.help_page.bind("h", self.close_help)
		self.credits_linkedname.bind("<1>", open_webpage)
		
		self.hotkeys1.config(text=
								"<s>" +"\n"+
								"← →" +"\n"+
								"↵" +"\n"+ #↵
								lang[my_language]["doubleclick"] +"\n"+
								"<f>     <F11>" +"\n"+
								"<Esc>" +"\n"+
								lang[my_language]["page"] +"\n"+
								"<3>    <6>" +"\n"+
								"<h>" +"\n"+
								"<r>")

		self.hotkeys2.config(text=
								lang[my_language]["settings"] +"\n"+
								lang[my_language]["next_page"] +"\n"+
								lang[my_language]["hide_show_b"] +"\n"+
								lang[my_language]["hide_show_b"] +"\n"+
								lang[my_language]["fullscreen_onoff"] +"\n"+
								lang[my_language]["fullscreen_esc"] +"\n"+
								lang[my_language]["3hourl6hourl"] +"\n"+
								lang[my_language]["3hourl6hourl"] +"\n"+
								lang[my_language]["help"] +"\n"+
								lang[my_language]["reload"])
		
		
		self.credits1.config(text="Developed by")
		self.credits_linkedname.config(text="Jan-Patrick Tyra")
		self.credits2.config(text=
							#"https://github.com/jiavu" +"\n\n"+
							"Ver. "+ infobox_version +" - "+ release_date +"\n\n"+
							"weather data from" +"\n"+
							"openweathermap.org")		#https://openweathermap.org/
							#"weather icons by Starder, http://freedesignfile.com" +"\n"+
							#"wind vanes by Jan-Patrick Tyra" +"\n\n"+
							#"Written in Python 3.6.5" +"\n\n"+
							
		
		
		Label(self.help_page, bg=main_bg_color, fg=main_fg_color, font=(set_font, 12, "bold"), text=lang[my_language]["help"]).grid(row=0, column=0, columnspan=2, pady=5)
		# Label(self.help_page, bg=main_bg_color, font=(set_font, 8)).pack()
		Label(self.help_page, bg=main_bg_color, fg=main_fg_color, font=(set_font, 10, "bold"), text="Hotkeys:").grid(row=1, column=0, sticky=W, padx=10)
		self.hotkeys.grid(row=2, column=0, rowspan=2, padx=8, pady=10)
		self.hotkeys1.pack(padx=8, pady=8, side=LEFT)
		self.hotkeys2.pack(padx=8, pady=8, side=LEFT)
		#Label(self.help_page, bg=main_bg_color, font=(set_font, 8)).pack(side=LEFT)
		self.credits.grid(row=2, column=1, padx=8, pady=10)
		self.credits1.pack()
		self.credits_linkedname.pack()
		self.credits2.pack()
		#Label(self.help_page, bg=main_bg_color, font=(set_font, 8)).pack()
		self.close.grid(row=3, column=1)
	
	
	def close_help(self, *args):
		self.help_page.destroy()
		key_control.state_help = False
	



class BackFrame:		# Only for Win sys. Failed test so far.
	
	""" I tried to get a transparent background for the interface. Not 100% transparent but with a lower opacity.
It would be nice if the interface gets a kind of Windows aero-design (blurred, transparent). Maybe Pillow can help but I'm not sure.
I also wished to deactivate the title bar by overrideredirect but after doing this you can't move the window anymore.

Why did I create a 2nd window named 'backframe'?
It's because you can activate transparency and background will disappear but you can't lower the opcatiy for background only.
When lowering the opacity it takes effect on the whole interface on Windows.
The 'backframe' below follows the position of 'window' but backframe won't stay directly behind window all the time.

"""
	
	def __init__(self):
		
		backframe["bg"] = "black"
		#backframe.overrideredirect(True)
		backframe.attributes("-toolwindow", True)
		backframe.wm_attributes("-alpha", 0.9)
		
		window.wm_attributes("-transparentcolor", main_bg_color)
		#window.overrideredirect(True)
		window.attributes("-toolwindow", True)
		window.attributes("-topmost", True)
		
		self.get_position()
	
	def get_position(self):
		backframe.geometry(window.winfo_geometry())
		backframe.lower(window)		# The backframe doesn't stay behind window... :/
		window.lift(backframe)
		
		
		backframe.after(10, self.get_position)
		
	
	
	
if __name__ == "__main__":
	window = Tk()
	#backframe = Tk()	# Windows only
	window.title("Infobox "+ infobox_version)
	window["bg"] = main_bg_color
	window.geometry("480x320+0+0")
	#window.geometry("480x320+1100+510") # width x height + x_offset + y_offset: (Setze auf 480x320). Der Offset ist der Abstand zum Desktop-Rand.
	# window.overrideredirect(True) # overrides titlebar.
	# window.state("zoomed") # Funktioniert nur für Windows. Maximiert das Fenster. Dazu noch overrideredirect, dann hat man quasi Fullscreen.
	# window.attributes("-zoomed", True) # Sollte für Linux funktionieren. (+ overrideredirect)
	# IMPORTANT!!: Beende Programm zur Not mit Alt + F4.

	# window.attributes("-fullscreen", True) # oder window.wm_attributes("-fullscreen", True)
	window.resizable(width=False, height=False)
	#window["cursor"] = "plus"
	window["cursor"] = "arrow"
	
	
	# global variables:
	hf = False
	switch_view = 1
	c_dt = "--:--"
	current_data = {}
	forecast_data = {}
	offline_state = False
	no_data = True
	my_language = "en"
	unit_temp1 = "°"
	unit_temp2 = "°C"
	unit_speed = " m/s"
	
	
	uhr = Uhr()
	weather_app = WeatherApp()
	settings_and_import = SettingsAndImport()
	help_and_credits = HelpAndCredits()
	key_control = KeyControl()
	
	#back_frame = BackFrame() # Failed transparency test. For Windows system only.
	
	window.mainloop()
	#backframe.mainloop()