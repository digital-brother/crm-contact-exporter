from hubspot import HubSpot

api_client = HubSpot(
    access_token="eu1-a7ab-3715-4b95-9f5f-53b730d11c3c")

api_client.access_token = "pat-eu1-8b6c2f2f-d75e-46b1-8a00-338ec3f66062"

hubspot_list = api_client.crm.contacts.get_all()
contacts = {}

for item in hubspot_list:
    contacts['email'] = item.properties['email']
    contacts['firstname'] = item.properties['firstname']
    contacts['lastname'] = item.properties['lastname']
    print(contacts)
print(contacts, 'contacts22')

# for contact in data:
#     contacts = contact.to_dict()
#     x = pd.DataFrame([contacts['properties']]).drop(columns=['hs_object_id', 'createdate', 'lastmodifieddate'],
#                                                     axis=3)
#     c.append(x)
# with open('some.csv', 'w', newline='') as f:
#     writer = csv.writer(f)
#     for c in contacts:
#         print(c)
