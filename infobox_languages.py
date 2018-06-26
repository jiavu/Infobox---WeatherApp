"""
My application has a multilingual support :)

Feel free to add other languages!

My app makes an URL request to openweathermap.org containing a language call in ISO 639-1 but
translation is only applied for the weather "description" field! I. e. wind description is excluded.

They support the following languages that you can use with the corresponded lang values: 
Arabic - ar, Bulgarian - bg, Catalan - ca, Czech - cz, German - de, Greek - el, English - en,
Persian (Farsi) - fa, Finnish - fi, French - fr, Galician - gl, Croatian - hr, Hungarian - hu,
Italian - it, Japanese - ja, Korean - kr, Latvian - la, Lithuanian - lt, Macedonian - mk, Dutch - nl,
Polish - pl, Portuguese - pt, Romanian - ro, Russian - ru, Swedish - se, Slovak - sk, Slovenian - sl,
Spanish - es, Turkish - tr, Ukrainian - ua, Vietnamese - vi, Chinese Simplified - zh_cn,
Chinese Traditional - zh_tw.
[15 June 2018]


Manual:
You can add other languages by adding a new dictionary in the 'lang' dictionary.
Just copy one of the dictionaries inside the 'lang' dictionary, paste it inside the 'lang' dictionary
before last '}' and replace the values on the right side with your translation.

Please name the new dictionary as 639-1 language code ("en" for English):
If you copied a language dictionary and pasted it below the others, replace the first key with the new
language code.

Don't change the other left side words (the keys), they are reference!

Don't forget the "quotes", we need strings here!
Don't delete commas - otherwise the dictionary will be broken.


I recommend to check if the dictionary package has no syntax errors by executing infobox_languages.py.
In the main file of infobox you won't see if the dictionary is okay because it's called in a try/except.
"""

lang = {

# ENGLISH:

"en" : {

		"hours_minutes" : "%I.%M %p",					# time formatting see https://docs.python.org/3/library/time.html#time.strftime
		"hours_minutes2" : "%I.%M %p",					# Shown on page2, current time of the timezone
		"hour" : ":00",									# range(24):00
		"weekday_and_date" : "{weekday} %d {month} %Y",
		"weekday" : {									# Set 0 and 7 to Sunday!
						"0" : "Sunday",
						"1" : "Monday",
						"2" : "Tuesday",
						"3" : "Wednesday",
						"4" : "Thursday",
						"5" : "Friday",
						"6" : "Saturday",
						"7" : "Sunday"
						},
		"month" : {
						"01" : "January",
						"02" : "February",
						"03" : "March",
						"04" : "April",
						"05" : "May",
						"06" : "June",
						"07" : "July",
						"08" : "August",
						"09" : "September",
						"10" : "October",
						"11" : "November",
						"12" : "Dezember"
						},
		"week_number" : "WN {}",						# (calendar week number of the year)
		"wind_direction" : {
						"-" : "-",
						"N" : "north",
						"NE": "northeast",
						"E" : "east",
						"SE": "southeast",
						"S" : "south",
						"SW": "southwest",
						"W" : "west",
						"NW": "northwest"
						},
		"wind_description" : {							# look for https://en.wikipedia.org/wiki/Beaufort_scale article in your language
						"--"   : "--",
						"0Bft" : "Calm",
						"1Bft" : "Light air",
						"2Bft" : "Light breeze",
						"3Bft" : "Gentle breeze",
						"4Bft" : "Moderate breeze",
						"5Bft" : "Fresh breeze",
						"6Bft" : "Strong breeze",
						"7Bft" : "Moderate gale",
						"8Bft" : "Fresh gale",
						"9Bft" : "Strong gale",
						"10Bft": "Storm",
						"11Bft": "Violent storm",
						"12Bft": "Hurricane"
						},
		"wind_format" : "{wind_description} from the {wind_direction}",
		"sunrise_sunset" : "↑ {}, ↓ {}",			# ↑↓
		"clouds" : "{}% clouds",
		"clouds2" : "{}% clouds",						# abbreviated if longer than 5 digits
		"wind_speed" : "Wind speed: {speed}{u}",
		"visibility" : "{} km visibility",
		"temp_rest_day" : "rest of today: {max}{u} / {min}{u}",
		"humidity" : "Humidity: {}%",
		"tomorrow" : "Tomorrow:",
		"night" : "Night",
		"morning" : "Morning",
		"noon" : "Noon",
		"evening" : "Evening",

		"settings" : "Settings",
		"next_page" : "Next page",
		"hide_show_b" : "Hide/show buttons",
		"fullscreen_onoff" : "Fullscreen on/off",
		"fullscreen_esc" : "Exit fullscreen",
		"3hourl6hourl" : "3 or 6 hourly forecast",
		"help" : "Help",
		"reload" : "Reload",
		"doubleclick" : "Doubleclick",
		"page" : "Page ↑ ↓",
		"close" : "Close",

		"error" : 'Error: "',
		"place_missing" : "Please enter a place",
		"api_missing" : "Please enter a valid API key",
		"not_found" : "Does this place really exist?",
		"unauthorized" : "Is your API key correct?",
		"connection" : "Am I connected to the internet?",
		"other" : "Something went wrong :/",
		"numbers" : "Only numbers accepted for City ID",
		"write_save" : "Couldn't write save file",
		
		"cityid" : "City ID",
		"timezone" : "Timezone",
		"search" : "Search",
		"search_by" : "Search location by:",
		"get_key" : "get a key from\n openweathermap.org",		# Please place a \n (New line)
		"api_key" : "API key",
		"city_name" : "City name, country code",
		"zip" : "ZIP, country code",
		"auto" : "Automatically (IP)"


		},


# GERMAN:

"de" : {

		"hours_minutes" : "%H:%M",						# time formatting see https://docs.python.org/3/library/time.html#time.strftime
		"hours_minutes2" : "%H:%M Uhr",					# Shown on page2, current time of the timezone
		"hour" : " Uhr:",								# range(24):00
		"weekday_and_date" : "{weekday}, %d. {month} %Y",
		"weekday" : {									# Set 0 and 7 to Sunday!
						"0" : "Sonntag",
						"1" : "Montag",
						"2" : "Dienstag",
						"3" : "Mittwoch",
						"4" : "Donnerstag",
						"5" : "Freitag",
						"6" : "Samstag",
						"7" : "Sonntag"
						},
		"month" : {
						"01" : "Januar",
						"02" : "Februar",
						"03" : "März",
						"04" : "April",
						"05" : "Mai",
						"06" : "Juni",
						"07" : "Juli",
						"08" : "August",
						"09" : "September",
						"10" : "Oktober",
						"11" : "November",
						"12" : "Dezember"
						},
		"week_number" : "KW {}",						# (calendar week number of the year)
		"wind_direction" : {
						"-" : "-",
						"N" : "Nord",
						"NE": "Nordost",
						"E" : "Ost",
						"SE": "Südost",
						"S" : "Süd",
						"SW": "Südwest",
						"W" : "West",
						"NW": "Nordwest"
						},
		"wind_description" : {							# look for https://en.wikipedia.org/wiki/Beaufort_scale article in your language
						"--"   : "--",
						"0Bft" : "Windstill",
						"1Bft" : "geringer Wind",
						"2Bft" : "leichter Wind",
						"3Bft" : "schwacher Wind",
						"4Bft" : "mäßiger Wind",
						"5Bft" : "frischer Wind",
						"6Bft" : "starker Wind",
						"7Bft" : "stark bis stürmischer Wind",
						"8Bft" : "stürmischer Wind",
						"9Bft" : "Sturm",
						"10Bft": "schwerer Sturm",
						"11Bft": "orkanartiger Sturm",
						"12Bft": "Orkan"
						},
		"wind_format" : "{wind_description} aus {wind_direction}",
		"sunrise_sunset" : "↑ {} Uhr, ↓ {} Uhr",
		"clouds" : "{}% Bewölkung",
		"clouds2" : "{}% Bw.",							# abbreviated if longer than 5 digits
		"visibility" : "{} km Sichtweite",
		"wind_speed" : "Windgeschwindigkeit: {speed}{u}",
		"temp_rest_day" : "Temp. restl. Tag: {max}{u} / {min}{u}",
		"humidity" : "Luftfeuchte: {}%",
		"tomorrow" : "Morgen:",
		"night" : "Nachts",
		"morning" : "Morgens",
		"noon" : "Mittags",
		"evening" : "Abends",

		"settings" : "Einstellungen",
		"next_page" : "Nächste Seite",
		"hide_show_b" : "Buttons ein-/ausblenden",
		"fullscreen_onoff" : "Vollbild an/aus",
		"fullscreen_esc" : "Vollbild beenden",
		"3hourl6hourl" : "3-stündl./6-stündl. Prognose",
		"help" : "Hilfe",
		"reload" : "Neu laden",
		"doubleclick" : "Doppelklick",
		"page" : "Bild ↑ ↓",
		"close" : "Schließen",

		"error" : 'Fehler: "',
		"place_missing" : "Bitte Ort angeben",
		"api_missing" : "API-Key fehlt",
		"not_found" : "Existiert dieser Ort wirklich?",
		"unauthorized" : "Ist dein API-Key korrekt?",
		"connection" : "Hast du eine Internetverbindung?",
		"other" : "Irgendwas ist schief gelaufen :/",
		"numbers" : "City-ID: nur Zahlen akzeptiert",
		"write_save" : "Fehler beim Schreiben der Speicherdatei",
		
		"cityid" : "City-ID",
		"timezone" : "Zeitzone",
		"search" : "Suche",
		"search_by" : "Ort auswählen nach:",
		"get_key" : "anfordern auf\n openweathermap.org",		# Please place a \n (New line)
		"api_key" : "API-Key",
		"city_name" : "Ortsname, Ländercode",
		"zip" : "ZIP (PLZ), Ländercode",
		"auto" : "Automatisch (IP)"

		},


# FRENCH:

"fr" : {

		"hours_minutes" : "%H h %M",					# time formatting see https://docs.python.org/3/library/time.html#time.strftime
		"hours_minutes2" : "%H h %M",					# Shown on page2, current time of the timezone
		"hour" : " h:",								# range(24):00
		"weekday_and_date" : "{weekday} %d {month} %Y",
		"weekday" : {									# Set 0 and 7 to Sunday!
						"0" : "dimanche",
						"1" : "lundi",
						"2" : "mardi",
						"3" : "mercredi",
						"4" : "jeudi",
						"5" : "vendredi",
						"6" : "samedi",
						"7" : "dimanche"
						},
		"month" : {
						"01" : "janvier",
						"02" : "février",
						"03" : "mars",
						"04" : "avril",
						"05" : "mai",
						"06" : "juin",
						"07" : "juillet",
						"08" : "août",
						"09" : "septembre",
						"10" : "Octobre",
						"11" : "novembre",
						"12" : "décembre"
						},
		"week_number" : "Semaine {}",						# (calendar week number of the year)
		"wind_direction" : {
						"-" : "-",
						"N" : "du nord",
						"NE": "du northeast",
						"E" : "de l'est",
						"SE": "du sud-est",
						"S" : "du sud",
						"SW": "du sud-ouest",
						"W" : "de l'ouest",
						"NW": "du nord-ouest"
						},
		"wind_description" : {							# look for https://en.wikipedia.org/wiki/Beaufort_scale article in your language
						"--"   : "--",
						"0Bft" : "Calme",
						"1Bft" : "Très légère brise",
						"2Bft" : "Légère brise",
						"3Bft" : "Petite brise",
						"4Bft" : "Jolie brise",
						"5Bft" : "Bonne brise",
						"6Bft" : "Vent frais",
						"7Bft" : "Grand frais",
						"8Bft" : "Coup de vent",
						"9Bft" : "Fort coup de vent",
						"10Bft": "Tempête",
						"11Bft": "Violente tempête",
						"12Bft": "Ouragan"
						},
		"wind_format" : "{wind_description} {wind_direction}",
		"sunrise_sunset" : "↑ {}, ↓ {}",			# ↑↓
		"clouds" : "{}% nuageux",					# nuages?
		"clouds2" : "{}% nuag.",					# abbreviated if longer than 5 digits
		"visibility" : "{} km visibilité",
		"wind_speed" : "vitesse du vent: {speed}{u}",
		"temp_rest_day" : "reste de la journée: {max}{u} / {min}{u}",
		"humidity" : "humidité: {}%",
		"tomorrow" : "demain:",
		"night" : "nuit",
		"morning" : "matin",
		"noon" : "midi",
		"evening" : "soir",

		"settings" : "paramètres",
		"next_page" : "prochaine page",
		"hide_show_b" : "cacher ou montrer des boutons",
		"fullscreen_onoff" : "plein écran",
		"fullscreen_esc" : "quitter le mode plein écran",
		"3hourl6hourl" : "prévisions sur 3 ou 6 heures",
		"help" : "Aide",
		"reload" : "mettre à jour",
		"doubleclick" : "double-clic",
		"page" : "Page ↑ ↓",
		"close" : "Fermer",

		"error" : 'Error: "',
		"place_missing" : "Please enter a place",
		"api_missing" : "Please enter a valid API key",
		"not_found" : "Does this place really exist?",
		"unauthorized" : "Is your API key correct?",
		"connection" : "Am I connected to the internet?",
		"other" : "Quelque chose a mal tourné :/",
		"numbers" : "Only numbers accepted for City ID",
		"write_save" : "Couldn't write save file",
		
		"cityid" : "City ID",
		"timezone" : "fuseau horaire",
		"search" : "Search",
		"search_by" : "Search location by:",
		"get_key" : "optenir un key de\n openweathermap.org",		# Please place a \n (New line)
		"api_key" : "API key",
		"city_name" : "nom de lieu, code du pays",			# ou 'toponyme'?
		"zip" : "ZIP, code du pays",
		"auto" : "automatiquement (IP)"
		
		}

}



# ###########################################
print("Language package is okay, no syntax errors.")
print("Languages in package:")
for ln in lang:
	if len(lang[ln]) < 50:
		print(ln, len(lang[ln]), "items,", (50-len(lang[ln])), "item(s) missing!")
	else:
		print(ln, len(lang[ln]), "items")