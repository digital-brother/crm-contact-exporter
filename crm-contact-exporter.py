from datetime import date

import requests
from hubspot import HubSpot
import pandas as pd
from simple_salesforce import Salesforce

import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
env = os.environ

today = date.today()

client_id = env.get("ZOHO_CLIENT_ID")
client_secret = env.get("ZOHO_CLIENT_SECRET")
redirect_uri = env.get("ZOHO_REDIRECT_URI")
code = env.get("ZOHO_CODE")
zoho_access_token_url = env.get("ZOHO_ACCESS_TOKEN_URL")
zoho_contacts_url = env.get("ZOHO_CONTACTS_URL")

hubspot_access_token = env.get("HUBSPOT_ACCESS_TOKEN")

username = env.get("SALESFORCE_USERNAME")
password = env.get("SALESFORCE_PASSWORD")
security_token = env.get("SALESFORCE_SECURITY_TOKEN")
instance_url = env.get("SALESFORCE_INSTANCE_URL")


def get_zoho_access_token():
    payload = {'grant_type': 'authorization_code',
               'client_id': client_id,
               'client_secret': client_secret,
               'redirect_uri': redirect_uri,
               'code': code}

    response = requests.request("POST", zoho_access_token_url, headers={}, data=payload, files=[])

    data = response.json()

    access_token = data['access_token']

    return access_token


def get_contacts_from_zoho():
    access_token = get_zoho_access_token()

    headers = {
        'Authorization': f'Zoho-oauthtoken {access_token}'
    }

    response = requests.request("GET", zoho_contacts_url, headers=headers, data={}, files=[])

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
        access_token=hubspot_access_token)

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
    salesforce_credentials = Salesforce(username=username,
                                        password=password,
                                        security_token=security_token,
                                        instance_url=instance_url)

    contacts_data = salesforce_credentials.query_all("SELECT Department, Name, Email, Phone, Title FROM Contact")

    salesforce_contacts_df = pd.DataFrame(contacts_data['records']).drop(columns='attributes')
    salesforce_contacts_df.to_csv(f"reports/salesforce_contacts-{today}.csv", index=False)

    return salesforce_contacts_df


get_contacts_from_zoho()
get_contacts_from_hubspot()
get_contacts_from_salesforce()
