import pandas as pd
from pyscript import Element
from pyodide_http import patch_all
patch_all()

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

def reset_handler(event = None):
    if event:
        form_values = {
            "name": "", "email": "", "phone": "", "street": "", "city": "", "state": "", "zip": "", "country": "", "website": ""
        }
        display(f"Reset", target="message")         
        
# Map event handlers to elements

Element("name").element.oninput = name_input_handler
Element("email").element.oninput = email_input_handler
Element("phone").element.oninput = phone_input_handler
Element("street").element.oninput = street_input_handler
Element("city").element.oninput = city_input_handler
Element("state").element.oninput = state_input_handler
Element("zip").element.oninput = zip_input_handler
Element("country").element.oninput = country_handler
Element("website").element.oninput = website_input_handler
Element("form").element.onsubmit = submit_handler
Element("form").element.onreset = reset_handler

# Functions

# function to manually add rows to the result
def addRow():
    global result
    result = result.concat(form_values, ignore_index=True)
    message = Element("message")
    reset_handler()
    message.write("Row successfully added")
    return result

# write df to paragraph
def updateTable():
    sheet = Element("sheet")
    sheet.write(result)