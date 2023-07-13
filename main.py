from pyodide.ffi.wrappers import add_event_listener
from js import document
import pandas as pd
import panel as pn
from io import StringIO

result = pd.DataFrame()

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

def setup_handler():
    document.getElementById("startup").value = 'Ready'
        
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