vulcan2calendar
===============
script used to port exams from vulcan gradebook to a google calendar.
# Requirements
used packages:
```python
vulcan api library:
    vulcan-api
    (https://github.com/kapi2289/vulcan-api)

google api libraries:
    google-api-python-client
    google-auth-httplib2 
    google-auth-oauthlib
```
# Set up
### Vulcan
[vulcan-api setup guide](https://vulcan-api.readthedocs.io/en/latest/getting-started.html)  
### tl;dr
### create keystore
```python
from vulcan import Keystore

keystore = Keystore.create()

keystore = Keystore.create(device_model="Vulcan API")
with open("keystore.json", "w") as f:
    f.write(keystore.as_json)
```

### register account/device
```python
from vulcan import Account

# keystore read from cachefile, token symbol and pin avaliable on vulcan portal
account = Account.register(keystore, token, symbol, pin)
with open("account.json", "w") as f:
    f.write(account.as_json)
```

### Google
[google's guide](https://developers.google.com/calendar/api/quickstart/python)
### tl;dr
### install packages
```bash
  pip3 install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
### set up credentials and service account
[google guide](https://developers.google.com/workspace/guides/create-credentials)  
save credentials json file as ``credentials.json``
