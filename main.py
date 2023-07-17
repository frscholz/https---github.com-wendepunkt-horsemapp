from pyodide.ffi.wrappers import add_event_listener
from js import document
import pandas as pd
import panel as pn
from io import StringIO
import time
import pyodide_http
import requests
pyodide_http.patch_all()

result = pd.DataFrame()

url_values = {
    "keyword": "",
    "api_key": ""
}

form_values = {
    "name": "",
    "email": "", 
    "phone": "", 
    "street": "", 
    "city": "", 
    "state": "", 
    "zip": "", 
    "country": "", 
    "website": ""
}

# Event handlers

def name_input_handler(event = None):
    if event:
        form_values["name"] = event.target.value

def email_input_handler(event = None):
    if event:
        form_values["email"] = event.target.value        

def phone_input_handler(event = None):
    if event:
        form_values["phone"] = event.target.value

def street_input_handler(event = None):
    if event:
        form_values["street"] = event.target.value

def city_input_handler(event = None):
    if event:
        form_values["city"] = event.target.value

def state_input_handler(event = None):
    if event:
        form_values["state"] = event.target.value        

def zip_input_handler(event = None):
    if event:
        form_values["zip"] = event.target.value

def country_handler(event = None):
    if event:
        form_values["country"] = event.target.value

def website_input_handler(event = None):
    if event:
        form_values["website"] = event.target.value
        
def submit_handler(event = None):
    if event:
        event.preventDefault()
        addRow(form_values)
        display(f"{form_values['name']} added succesfully", target="message")

def reset_handler():
    form_values = {
        "name": "", "email": "", "phone": "", "street": "", "city": "", "state": "", "zip": "", "country": "", "website": ""
    }
    document.getElementById('name').value = ''
    document.getElementById('email').value = ''
    document.getElementById('phone').value = ''
    document.getElementById('street').value = ''
    document.getElementById('city').value = ''
    document.getElementById('state').value = ''
    document.getElementById('zip').value = ''
    document.getElementById('country').value = ''
    document.getElementById('website').value = ''

def setup_handler():
    document.getElementById("startup").value = 'Ready'

def key_input_handler(event = None):
    if event:
        url_values["api_key"] = event.target.value

def query_input_handler(event = None):
    if event:
        url_values["keyword"] = event.target.value
        
# Map event handlers to elements

Element("name").element.oninput = name_input_handler
Element("email").element.oninput = email_input_handler
Element("phone").element.oninput = phone_input_handler
Element("street").element.oninput = street_input_handler
Element("city").element.oninput = city_input_handler
Element("state").element.oninput = state_input_handler
Element("zip").element.oninput = zip_input_handler
add_event_listener(document.getElementById("country"), "change", country_handler)
Element("website").element.oninput = website_input_handler
Element("form").element.onsubmit = submit_handler
add_event_listener(document.getElementById("download"), "change", setup_handler)
Element("key").element.oninput = key_input_handler
Element("queries").element.oninput = query_input_handler

# function to manually add rows to the result
def addRow():
    global result
    # add check to see if form_values is empty
    result = result.append(form_values, ignore_index = True)
    reset_handler()
    display("Row successfully added", target="message")
    return result

# write df to paragraph
def updateTable():
    sheet = Element("sheet")
    sheet.clear()
    sheet.element.innerHTML = result.to_html()

# download csv
def get_csv():
    global result
    return io.BytesIO(result.to_csv().encode())

file_download_csv = pn.widgets.FileDownload(filename="data.csv", callback=get_csv, button_type="primary")    
success = pn.pane.Alert("Ready", alert_type="success")
pn.Column(file_download_csv).servable(target="download")
pn.Column(success).servable(target="startup")

# Googlemaps Script
baseurl = "https://proxy.cors.sh/https://maps.googleapis.com/maps/api/place/nearbysearch/"
placeurl = "https://proxy.cors.sh/https://maps.googleapis.com/maps/api/place/details/"
headers = {
            'x-cors-api-key': 'temp_178bccf5526e5262d160ee983995c4ae'
        }
payload = {}
radius = 20000

# please refer to googlemaps.py script for more readable code. 
def runScript():
    global result
    display("Running script...", target="output")
    coordinates = pd.read_csv('coordinates.csv')
    temp = coordinates.apply(lambda row: getPlaces((row["latitude"], row["longitude"])), axis=1)
    places = pd.DataFrame()
    for i in range(len(temp)):
        temp2 = pd.DataFrame.from_dict(temp[i]) # TODO: Error here
        places = pd.concat([places, temp2], ignore_index=True) 
    places.drop_duplicates(['place_id'])
    places2 = pd.DataFrame()
    places2 = places.apply(lambda row: getPlaceDetails(row['place_id']), axis=1)
    normalized = pd.json_normalize(places2)
    result = pd.concat([result, normalized], ignore_index=True)
    Element("output").clear()
    display("Script done!", target="output")

def getPlaceDetails(place_id):
    return place_id

def getPlaces(location):
    places = []
    url = baseurl + "json?location=" + str(location[0]) + "%2C" + str(location[1]) + "&radius=" + str(radius) + "&keyword=" + url_values["keyword"] + "&key=" + url_values["api_key"]
    response = requests.get(url, headers=headers, data=payload)
    response_data = response.json()
    places = places + response_data['results']
    while('next_page_token' in response_data):
        time.sleep(2)
        next_url = baseurl + "json?pagetoken=" + response_data['next_page_token']
        response = requests.get(next_url, headers=headers)
        response_data = response.json()
        places = places + response_data['results']
    return places    


def getPlaceDetails(place_id):
    fields = "place_id%2Cname%2Cformatted_address%2Cformatted_phone_number%2Crating%2Cwebsite%2Copening_hours"
    url = placeurl + "json?place_id=" + place_id + "&fields=" + fields + "&key=" + url_values["api_key"]
    response = requests.get(url, headers=headers, data=payload)
    response_data = response.json()
    return response_data['result']