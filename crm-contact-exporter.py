from datetime import date

import requests
from hubspot import HubSpot
import pandas as pd
from simple_salesforce import Salesforce
from sf_login import *

today = date.today()


def get_contacts_from_zoho():
    url = "https://accounts.zoho.eu/oauth/v2/token"

    payload = {'grant_type': 'authorization_code',
               'client_id': '1000.GJW951HCMON3OZ49YLEO1JZC0HCUZY',
               'client_secret': '0d36b23770308027169350713b92a02e3c6d9efcc1',
               'redirect_uri': 'http://localhost:8000/test',
               'code': '1000.cf449a8b14f0429ec8edac6b9cd3e690.ba0a5a149f2975ad4f27d7e51d404cde'}
    files = []
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    data = response.json()
    access_token = data['access_token']

    url = "https://www.zohoapis.eu/crm/v2/Contacts"

    payload = {}
    files = []
    headers = {
        'Authorization': f'Zoho-oauthtoken {access_token}'
    }

    response = requests.request("GET", url, headers=headers, data=payload, files=files)

    zoho_list = response.json()
    data = zoho_list['data']
    contacts_list = []
    for contact in data:
        contacts = {'email': contact['Email'], 'firstname': contact['First_Name'], 'lastname': contact['Last_Name'],
                    'phone': contact['Phone'], 'title': contact['Title'], 'department': contact['Department']}
        contacts_list.append(contacts)
    contacts_zoho = pd.DataFrame(contacts_list).to_csv(f"reports/contacts_zoho-{today}.csv", index=False)

    return contacts_zoho


def get_contacts_from_hubspot():
    api_client = HubSpot(
        access_token="pat-eu1-8b6c2f2f-d75e-46b1-8a00-338ec3f66062")

    api_client.access_token = "pat-eu1-8b6c2f2f-d75e-46b1-8a00-338ec3f66062"

    hubspot_list = api_client.crm.contacts.get_all()
    # print(hubspot_list)

    contacts_list = []
    for contact in hubspot_list:
        contacts = {'email': contact.properties['email'], 'firstname': contact.properties['firstname'],
                    'lastname': contact.properties['lastname']}
        contacts_list.append(contacts)
    contacts_hubspot = pd.DataFrame(contacts_list).to_csv(f"reports/contacts_hubspot-{today}.csv", index=False)
    return contacts_hubspot


def get_contacts_from_salesforce():
    sf = Salesforce(username=username,
                    password=password,
                    security_token=token,
                    instance_url=instance)

    contacts_data = sf.query_all("SELECT Email, Phone, Name, Title, Department FROM Contact")
    contacts_sf = pd.DataFrame(contacts_data['records']).drop(columns='attributes').to_csv(f"reports/contacts_sf-{today}.csv",
                                                                                           index=False)
    return contacts_sf


get_contacts_from_zoho()
get_contacts_from_hubspot()
get_contacts_from_salesforce()

