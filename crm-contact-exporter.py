from datetime import date

import requests
from hubspot import HubSpot
import pandas as pd
from simple_salesforce import Salesforce

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


today = date.today()


def get_zoho_access_token():
    payload = {'grant_type': 'authorization_code',
               'client_id': os.environ.get("ZOHO_CLIENT_ID"),
               'client_secret': os.environ.get("ZOHO_CLIENT_SECRET"),
               'redirect_uri': os.environ.get("ZOHO_REDIRECT_URI"),
               'code': os.environ.get("ZOHO_CODE")}

    response = requests.request("POST", os.environ.get("ZOHO_ACCESS_TOKEN_URL"), headers={}, data=payload, files=[])

    data = response.json()

    access_token = data['access_token']

    return access_token


def get_contacts_from_zoho():
    access_token = get_zoho_access_token()

    headers = {
        'Authorization': f'Zoho-oauthtoken {access_token}'
    }

    response = requests.request("GET", os.environ.get("ZOHO_CONTACTS_URL"), headers=headers, data={}, files=[])

    zoho_list = response.json()

    data = zoho_list['data']

    contacts_list = []

    for contact in data:
        contacts = {'Department': contact['Department'], 'First name': contact['First_Name'],
                    'Last name': contact['Last_Name'], 'Email': contact['Email'],
                    'Phone': contact['Phone'], 'Title': contact['Title']}
        contacts_list.append(contacts)

    zoho_contacts_df = pd.DataFrame(contacts_list)
    zoho_contacts_df.to_csv(f"reports/zoho_contacts-{today}.csv", index=False)

    return zoho_contacts_df


def get_contacts_from_hubspot():
    api_client = HubSpot(
        access_token=os.environ.get("HUBSPOT_ACCESS_TOKEN"))

    hubspot_list = api_client.crm.contacts.get_all()

    contacts_list = []
    for contact in hubspot_list:
        contacts = {'First name': contact.properties['firstname'], 'Last name': contact.properties['lastname'],
                    'Email': contact.properties['email']
                    }
        contacts_list.append(contacts)

    hubspot_contacts_df = pd.DataFrame(contacts_list)
    hubspot_contacts_df.to_csv(f"reports/contacts_hubspot-{today}.csv", index=False)

    return hubspot_contacts_df


def get_contacts_from_salesforce():
    sf = Salesforce(username=os.environ.get("SALESFORCE_USERNAME"),
                    password=os.environ.get("SALESFORCE_PASSWORD"),
                    security_token=os.environ.get("SALESFORCE_SECURITY_TOKEN"),
                    instance_url=os.environ.get("SALESFORCE_INSTANCE_URL"))

    contacts_data = sf.query_all("SELECT Department, Name, Email, Phone, Title FROM Contact")

    salesforce_contacts_df = pd.DataFrame(contacts_data['records']).drop(columns='attributes')
    salesforce_contacts_df.to_csv(f"reports/salesforce_contacts-{today}.csv", index=False)

    return salesforce_contacts_df


get_contacts_from_zoho()
get_contacts_from_hubspot()
get_contacts_from_salesforce()
