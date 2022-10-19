import requests
import geopy
from config.local_settings import mapquest_api

response = requests.get('https://www.cbr-xml-daily.ru/daily_json.js')
unparsed_content = response.json()

geolocator = geopy.Nominatim(user_agent=mapquest_api)
location = geolocator.reverse("52.509669, 13.376294")
