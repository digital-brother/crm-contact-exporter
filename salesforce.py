import pandas as pd
from simple_salesforce import Salesforce
from login import *

sf = Salesforce(username=username,
                password=password,
                security_token=token,
                instance_url=instance)


data = sf.query_all("SELECT Email, Phone, Name FROM Contact")
sf_df = pd.DataFrame(data['records']).drop(columns='attributes')
sf_df.to_csv('test.csv')


