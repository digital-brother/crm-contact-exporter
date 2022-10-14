from zcrmsdk import ZCRMRestClient, ZohoOAuth

config = {
    'sandbox': 'False',
    'apiBaseUrl': 'https://www.zohoapis.eu',
    'applicationLogFilePath': './log',
    'client_id': '1000.3N1PVITTA0GNC2F6U6AQLKSXR83PZH',
    'client_secret': '7fbaec564990bd6fdc911cc39156fef7fa9f519c22',
    'redirect_uri': 'http://localhost:8000/test',
    'account_url': 'https://accounts.zoho.eu/',
    'token_persistence_path': '.',
    'currentUserEmail': 'testsmtpmail1@ukr.net'
}

ZCRMRestClient.initialize(config)
oauth_client = ZohoOAuth.get_client_instance()
grant_token = "1000.63d5c901b996ebf1e1b03e3aee6218ce.93f305c55db244faa30875e35b6a7840"
oauth_tokens = oauth_client.generate_access_token(grant_token)

print(oauth_tokens)
