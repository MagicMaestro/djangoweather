from django.shortcuts import render
from datetime import datetime

# Create your views here.
def home(request):
	import json
	import requests

	aqi_userzip = '14210'

	if request.method == "POST":
		aqi_userzip = request.POST['aqi_zip']
	
	api_request = requests.get("https://www.airnowapi.org/aq/observation/zipCode/current/?format=application/json&zipCode=" + aqi_userzip + "&distance=5&API_KEY=74E24C77-996D-4ACA-B0F6-EFE61509DA66")

	try:
		api = json.loads(api_request.content)
	except Exception as e:
		api = "Error..."

	aqi_date = datetime.strptime(api[0]['DateObserved'].strip(), '%Y-%m-%d')
	aqi_time = str(api[0]['HourObserved']) + ':00'
	aqi_time = datetime.strptime(aqi_time, '%H:%M')

	if api[0]['Category']['Number'] == 1:
		aqi_class = 'aqi_good'
		aqi_desc = 'Good is a rating of 0 - 50'
		aqi_angle = '15'
	elif api[0]['Category']['Number'] == 2:
		aqi_class = 'aqi_moderate'
		aqi_desc = 'Moderate is a rating of 51 - 100'
		aqi_angle = '45'
	elif api[0]['Category']['Number'] == 3:
		aqi_class = 'aqi_usg'
		aqi_desc = 'Unhealthy for Sensitive Groups is a rating of 101 - 150'
		aqi_angle = '75'
	elif api[0]['Category']['Number'] == 4:
		aqi_class = 'aqi_unhealthy'
		aqi_desc = 'Unhealthy is a rating of 151 - 200'
		aqi_angle = '105'
	elif api[0]['Category']['Number'] == 5:
		aqi_class = 'aqi_vunhealthy'
		aqi_desc = 'Very Unhealthy is a rating of 201 - 300'
		aqi_angle = '135'
	elif api[0]['Category']['Number'] == 6:
		aqi_class = 'aqi_hazardous'
		aqi_desc = 'Hazardous is a rating of 301 - 500'
		aqi_angle = '175'
	else:
		aqi_class = 'aqi_unavail'
		aqi_desc = 'Air Quality information for this location is unavailable.'
		aqi_angle = false

	aqi_leg = [
		'0 - 50<span><br />Good</span>',
		'51 - 100<span><br />Moderate</span>',
		'101 - 150<span><br />USG</span>',
		'151 - 200<span><br />Unhealthy</span>',
		'201 - 300<span><br />Very Unhealthy</span>',
		'301 - 500<span><br />Hazardous</span>',
	]
	aqi = {
		'class': aqi_class,
		'rating': aqi_desc, 
		'date': aqi_date,
		'time': aqi_time,
		'legend': aqi_leg,
		'angle': aqi_angle,
		'zip': aqi_userzip,
	}

	return render(request, 'home.html', {'api': api, 'aqi': aqi})

def about(request):
	return render(request, 'about.html', {})